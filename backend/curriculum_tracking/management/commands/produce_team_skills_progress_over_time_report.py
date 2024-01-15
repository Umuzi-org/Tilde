from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum, AgileCard, RecruitProject
from core.models import Team, Stream, StreamCurriculum
from pathlib import Path
import pandas as pd
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("stream", type=str)
        parser.add_argument("team_name", type=str)

    def handle(self, *args, **options):
        name = options["stream"]
        team_name = options["team_name"]

        stream_curriculums = StreamCurriculum.objects.filter(stream__name=name)

        curriculum_list = []

        for stream_curriculum in stream_curriculums:
            curriculum_list.append(stream_curriculum.curriculum)

        print(curriculum_list)

        team = Team.objects.get(name=team_name)

        team_members = team.members

        team_emails = []

        for team_member in team_members:

            team_emails.append(team_member["user_email"])

        print(team_emails)

        content_items_list = []
        skills_name_and_amount = {}

        for curriculum in curriculum_list:

            for x in get_ordered_content_items(curriculum):

                if x.content_item.content_type == "P":

                    for s in x.content_item.tags.all():
                        if "skill/" in str(s):
                            content_items_list.append(x.content_item)
                            skills_name_and_amount[(str(s)[6:])] = skills_name_and_amount.get(
                                (str(s)[6:]), 0
                            )
                            skills_name_and_amount[(str(s)[6:])] += 1
                            break  # for now we assume that each content item falls only into one skill

        print("content items:")
        print(content_items_list)
        print()
        print("skills:")
        print(skills_name_and_amount)

        ######################

        # tried and failed to get the earliest date of first started card in the team (both by filtering the started
        # agile cards or the RecruitProject model - but hit walls both times so will make a dataframe)

        team_skills_cards = AgileCard.objects.filter(
            assignees__email__in=team_emails, content_item__in=content_items_list
        )


        # looking at all started cards

        # started_skills_cards = team_skills_cards.filter(recruit_project__isnull=False)

        #########################

        skills_data_list = []

        for email in team_emails:

            print(email)

            agile_cards = team_skills_cards.filter(assignees__email=email)

            for agile_card in agile_cards:
                if agile_card.recruit_project:
                    card_start = agile_card.recruit_project.start_time
                    card_end = agile_card.recruit_project.complete_time
                else:
                    card_start = None
                    card_end = None

                tags_list = [
                    (str(s)[6:])
                    for s in agile_card.content_item.tags.all()
                    if "skill/" in str(s)
                ]
                skill_tag = tags_list[0]

                skill_dict = {
                    "email": email,
                    "title": agile_card.content_item.title,
                    "status": agile_card.status,
                    "skill": skill_tag,
                    "card_start_time": card_start,
                    "card_end_date": card_end,
                }
                skills_data_list.append(skill_dict)

        if skills_data_list:

            skills_df = pd.DataFrame(skills_data_list)

            team_name_for_file = team_name.replace(" ", "_")

            skills_df.to_csv(f"gitignore/{team_name_for_file}_testing_skills.csv")

            ######

            # finding earliest start card
            earliest_card_start = skills_df[~skills_df.card_start_time.isna()][
                "card_start_time"
            ].min()

            # it is a string to convert to datetime to extract month and year? ALREADY IN RIGHT FORM
            # earliest_card_start_datetime = datetime.strptime(earliest_card_start, '%Y-%m-%d %H:%M:%S.%f%z')

            start_progress_tracking_date = datetime(
                earliest_card_start.year, earliest_card_start.month, 1
            )
            current_date = datetime.now()
            end_progress_tracking_date = datetime(
                current_date.year, (current_date.month), 1
            )

            # time increment
            one_month_increment = relativedelta(months=1)

            # skills list
            skills_list = list(skills_df.skill.unique())

            time_change = relativedelta(
                end_progress_tracking_date, start_progress_tracking_date
            )

            dates_string_list = []
            dates_datetime_list = []
            for date_increment in range(
                time_change.months + time_change.years * 12 + 2
            ):
                dates_string_list.append(
                    (
                        start_progress_tracking_date
                        + relativedelta(months=date_increment)
                    ).strftime("%Y-%m-%d")
                )
                dates_datetime_list.append(
                    start_progress_tracking_date + relativedelta(months=date_increment)
                )

            # function to remove time zone from dates
            def remove_timezone(row):
                row["card_end_date"] = row["card_end_date"].replace(tzinfo=None)
                return row

            skills_df.set_index("email", inplace=True, drop=True)

            progress_over_time_columns = ["skills"]
            progress_over_time_columns.extend(dates_string_list)

            progress_over_time_df = pd.DataFrame(columns=progress_over_time_columns)

            progress_over_time_v2_columns = ["date"]
            progress_over_time_v2_columns.extend(skills_list)
            progress_over_time_df_v2 = pd.DataFrame(columns=progress_over_time_v2_columns)

            for email in team_emails:

                temp_learner_skills_df = skills_df.loc[email]

                temp_learner_progress_over_time_df = pd.DataFrame(
                    index=dates_string_list, columns=list(skills_name_and_amount.keys())
                )
                temp_learner_progress_over_time_df.loc[:, :] = 0


                for skill in list(skills_name_and_amount.keys()):

                    temp_skill_df = temp_learner_skills_df[
                        temp_learner_skills_df["skill"] == skill
                    ]

                    number_of_projects_with_skill = skills_name_and_amount[skill]

                    # non_null complete entries
                    learner_completed_projects_with_skill = temp_skill_df[
                        temp_skill_df.card_end_date.notnull()
                    ]
                    # remove tz
                    learner_completed_projects_with_skill = (
                        learner_completed_projects_with_skill.apply(
                            remove_timezone, axis=1
                        )
                    )
                   
                    

                    for date in list(temp_learner_progress_over_time_df.index):

                        if len(learner_completed_projects_with_skill) > 0:
                            completed_cards_at_tracking_date = len(
                                learner_completed_projects_with_skill[
                                    learner_completed_projects_with_skill[
                                        "card_end_date"
                                    ]
                                    <= datetime.strptime(date, "%Y-%m-%d")
                                ]
                            )
                        else:
                            completed_cards_at_tracking_date = 0

                        percent_completed_cards_at_tracking_date = round(
                            (
                                completed_cards_at_tracking_date
                                / number_of_projects_with_skill
                            )
                            * 100
                        )



                        temp_learner_progress_over_time_df.loc[
                            date, skill
                        ] = percent_completed_cards_at_tracking_date



                temp_learner_progress_over_time_df_transposed = (
                    temp_learner_progress_over_time_df.T
                )
                temp_learner_progress_over_time_df_transposed.index.name = "skills"
                temp_learner_progress_over_time_df_transposed["learner"] = email
                temp_learner_progress_over_time_df_transposed.reset_index(inplace=True)
                temp_learner_progress_over_time_df_transposed.set_index(
                    "learner", inplace=True
                )
                temp_learner_progress_over_time_df_transposed.index.name = None

                progress_over_time_df = pd.concat(
                    [progress_over_time_df, temp_learner_progress_over_time_df_transposed]
                )

                #for v2 output
                temp_learner_progress_over_time_df["learner"] = email
                temp_learner_progress_over_time_df.index.name = "date"
                temp_learner_progress_over_time_df.reset_index(inplace=True)
                temp_learner_progress_over_time_df.set_index(
                    "learner", inplace=True)
                temp_learner_progress_over_time_df.index.name = None
                progress_over_time_df_v2 = pd.concat([progress_over_time_df_v2, temp_learner_progress_over_time_df])
                


            print(progress_over_time_df.head(30))
            progress_over_time_df.to_csv(f"gitignore/{team_name_for_file}_skills_progress_over_time.csv")

            print(progress_over_time_df_v2.head(30))
            progress_over_time_df_v2.to_csv(f"gitignore/{team_name_for_file}_skills_progress_over_time_v2.csv")

            skills_df.to_csv(f"gitignore/{team_name_for_file}_testing_skills.csv")

                

                
