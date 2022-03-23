from core.models import *
from curriculum_tracking.models import *
from django.db.models import Q

teams = Team.objects.filter(name__startswith="E1")
users = []

for team in teams:
    users.extend(team.user_set.all())

cards = (
    AgileCard.objects.filter(assignees__in=users)
    .filter(
        Q(status=AgileCard.IN_PROGRESS)
        | Q(status=AgileCard.IN_REVIEW)
        | Q(status=AgileCard.REVIEW_FEEDBACK)
    )
    .prefetch_related("content_item")
)

print("CARDS IN PROGRESS\n")
ip_content_items = [card.content_item for card in cards]
# for item in set(ip_content_items):
#     print(item)

# print("\nREADY CARDS\n")

ready_cards = []
for user in users:
    ready_cards.extend(
        [
            o.content_item
            for o in AgileCard.objects.filter(assignees__in=[user]).order_by("order")[
                :2
            ]
        ]
    )

# for item in set(ready_cards):
#     print(item)


for item in set(ready_cards + ip_content_items):
    url_end = item.url[len("http://syllabus.africacode.net/") :]
    full_url = f"https://github.com/Umuzi-org/ACN-syllabus/tree/develop/content/{url_end}_index.md"
    print(full_url)
