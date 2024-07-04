"""
python manage.py export_reviews_for_poor_mans_trust_prop percival.rapha@umuzi.org "Validate a South African ID number" "python"

"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from curriculum_tracking.models import RecruitProjectReview, AgileCard
from django.utils import timezone
import os

User = get_user_model()


def get_task_description(who, content_item_title, flavours, final):
    result = f""" 
# Docs


See 'Poor Man's trust prop' docs here: https://app.gitbook.com/o/2DzlYnPstQTFtiSgav55/s/QrgdShfgwVxn9oBO7tlc/reviewing-learner-projects/poor-mans-trust-propagation


# Nomination under review  


{who}
{content_item_title}
{', '.join(flavours)}    


# Reviews to be considered:


"""
    for card_id in final:
        result += (
            f"\nhttps://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card_id}"
        )

    return result


def task_exists(task_title):
    query = """
        query {
            boards(ids: [1424431962]) {
                name
                items_count
                items_page(limit: 500) {
                items {
                    name
                    column_values {
                        id
                        text
                    }
                }
                }
            }
        }
    """
    data = make_monday_query(query)["data"]
    item_count = data["boards"][0]["items_count"]
    assert (
        item_count < 500
    ), "need to implement pagination. see https://developer.monday.com/api-reference/docs/querying-board-items"

    items = data["boards"][0]["items_page"]["items"]
    items = [item for item in items if item["name"] == task_title]
    for item in items:
        for column_value in item["column_values"]:
            if column_value["id"] == "status" and column_value["text"] != "Done":
                # there is a TODO task that matches this name.
                return True
    return False


def make_monday_query(query):

    import requests

    apiKey = os.getenv("MONDAY_ACCESS_TOKEN")
    assert apiKey
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": apiKey, "API-Version": "2023-04"}

    data = {"query": query}

    response = requests.post(url=apiUrl, json=data, headers=headers)
    return response.json()


def create_task(task_title, task_description):
    breakpoint()
    create_task_mutation = (
        '''
        mutation {
            create_item(item_name:"'''
        + task_title
        + """",board_id:1424431962){
                id
            }
        }
    """
    )

    response_data = make_monday_query(create_task_mutation)

    item_id = response_data["data"]["create_item"]["id"]

    add_comment_mutation = (
        """
        mutation {
        create_update(item_id:"""
        + item_id
        + ''', body:"'''
        + task_description
        + """"){
            id
        }
        }
    """
    )
    response_data = make_monday_query(add_comment_mutation)


def create_monday_task(task_title, task_description):
    if task_exists(task_title):
        return
    create_task(task_title, task_description)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)
        parser.add_argument("content_item_title", type=str)
        parser.add_argument("flavour", type=str)

    def handle(self, *args, **options):
        who = options["who"]
        content_item_title = options["content_item_title"]
        flavours = [s for s in options["flavour"].split(",") if s]

        user = User.objects.get(email=who)
        reviews = (
            RecruitProjectReview.objects.filter(
                reviewer_user=user,
                recruit_project__content_item__title=content_item_title,
            )
            .filter(timestamp__gte=timezone.now() - timezone.timedelta(days=365))
            .order_by("-timestamp")
            .prefetch_related("recruit_project")
        )

        final = set()
        for review in reviews:
            project = review.recruit_project
            if project.flavours_match(flavours):
                try:
                    card = project.agile_card
                except AgileCard.DoesNotExist:
                    pass
                else:
                    final.add(card.id)
                    if len(final) > 10:
                        break
        task_description = get_task_description(
            who, content_item_title, flavours, final
        )
        task_title = f"{who} '{content_item_title}' {flavours}"
        create_monday_task(task_title, task_description)
        print(task_description)
