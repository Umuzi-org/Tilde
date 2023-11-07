from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum, AgileCard
from core.models import Team
from pathlib import Path
import pandas as pd


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("curriculum", type=str)
        parser.add_argument("team_name", type=str)

    def handle(self, *args, **options):
        name = options["curriculum"]
        team_name = options["team_name"]

        curriculum = Curriculum.objects.get(
            name=name
        )  # a stream is made up of mulitple curriculums, so getting one curriculum called in won't work to
        # traverse full course content, should update this to stream and then loop through each curriculum in the stream
        # however for now we will just filter agile cards for each team member to get the necessary content with the required
        # skills tags

        team = Team.objects.get(name=team_name)

        team_members = team.members

        # ***************************************************************************
        # AREN'T USING THIS SECTION FOR NOW

        titles_and_sections_dict = {}

        for x in get_ordered_content_items(curriculum):

            for s in x.content_item.tags.all():
                if "skill/" in str(s):
                    titles_and_sections_dict[x.content_item.title] = str(s)
                    break  # for now we assume that each content item falls only into one skill

        titles = titles_and_sections_dict.keys()
        skills = titles_and_sections_dict.values()

        headings = list(skills)

        # ****************************************************************************

        skills_data_list = []

        for team_member in team_members:

            agile_cards = AgileCard.objects.filter(
                assignees__email=team_member["user_email"]
            )

            for agile_card in agile_cards:

                if (
                    agile_card.content_item.content_type == "P"
                ):  # we are only tracking projects and not topics

                    tags_list = [
                        str(s)
                        for s in agile_card.content_item.tags.all()
                        if "skill/" in str(s)
                    ]
                    if tags_list:
                        skill_tag = tags_list[
                            0
                        ]  # only assuming one skill tag for now per content item
                        content_title = agile_card.content_item.title
                        status = agile_card.status
                        skill_dict = {
                            "email": team_member["user_email"],
                            "title": content_title,
                            "status": status,
                            "skill": skill_tag,
                        }
                        skills_data_list.append(skill_dict)

        if skills_data_list:

            skills_df = pd.DataFrame(skills_data_list)

            print(skills_df.head())

            skills_df.to_csv("gitignore/testing_skills.csv")

            progress_df_columns = ["email", "status"]
            progress_df_columns.extend(list(skills_df.skill.unique()))

            progress_df = pd.DataFrame(columns=progress_df_columns)

            for email in list(skills_df.email.unique()):
                print(email)
                temp_progress = (
                    skills_df.set_index("email", drop=True)
                    .loc[email]
                    .groupby(["status", "skill"])
                    .count()
                    .unstack()
                    .droplevel(0, axis=1)
                )
                temp_progress["email"] = email
                temp_progress.reset_index(inplace=True)
                temp_progress.set_index("email", drop=True, inplace=True)
                progress_df = pd.concat([progress_df, temp_progress]).fillna(0)

            progress_df.drop("email", axis=1, inplace=True)
            progress_df.to_csv("gitignore/curriculum_progress_report.csv")
            progress_df.to_excel(
                "gitignore/curriculum_progress_report.xlsx"
            )  # to get this line to work - i had to run this first: `pip install openpyxl`
