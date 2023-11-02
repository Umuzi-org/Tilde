from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum, AgileCard
from core.models import Team, User
import csv
from pathlib import Path
import pandas as pd


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("curriculum", type=str)
        parser.add_argument("team_name", type=str)

    def handle(self, *args, **options):
        name = options["curriculum"]
        team_name = options["team_name"]

        curriculum = Curriculum.objects.get(name=name)
        team = Team.objects.get(name=team_name)

        team_members = team.members

        titles_and_sections_dict = {}

        for x in get_ordered_content_items(curriculum):

            for s in x.content_item.tags.all():
                if "section/" in str(s):
                    titles_and_sections_dict[x.content_item.title] = str(s)
                    break

        headings = ["learner"]

        # currently this doesn't deal with section tag being used more than once, because order matters
        # i.e there will be a heading for each time a section tag is used
        titles = titles_and_sections_dict.keys()
        sections = titles_and_sections_dict.values()

        for section in sections:
            headings.append(section)

        # loop through all content items for a curriculum
        # find all that start with "skill/" and add to an array
        # order and remove duplicates   -----> this part is not done
        # create each skill as a heading

        # loop through each user in team
        # loop through each content item and fetch status and skill tags
        # update skill tags in table

        with open(Path(f"gitignore/{curriculum}_progress_report.csv"), "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)

            for team_member in team_members:
                print(f"email: {team_member['user_email']}")

                # agile_cards = AgileCard.objects.filter(
                #     assignees__email=team_member["user_email"]
                # )

                # print("all cards for this user")
                # for agile_card in agile_cards:
                #     print(agile_card.content_item.title)

                agile_cards = AgileCard.objects.filter(
                    assignees__email=team_member["user_email"],
                    content_item__title__in=titles,
                )

                status_list = []
                status_list.append(team_member["user_email"])

                for title in titles:

                    for agile_card in agile_cards.filter(
                        content_item__title__exact=title
                    ):
                        status = agile_card.status
                        status_list.append(status)
                        print(agile_card.content_item.title)
                        print(agile_card.status)

                writer.writerow(status_list)


# *****
# section = []

# for x in get_ordered_content_items(java_ncit):
#     section.append([str(s) for s in x.content_item.tags.all() if "section/" in str(s)])


# [item for item in section if len(item) != 0]

# [subitem for item in section for subitem in item]
