# """ Given the syllabus content and the progress of the recruit, what AgileCards should exist, and what should their status be?
# """
# from django.core.management.base import BaseCommand
# from curriculum_tracking import models
# from curriculum_tracking import helpers
# from curriculum_tracking import card_generation_helpers as gen_helpers
# from core import models as core_models
# import re


# def curriculum_users(curriculum):
#     for cohort in curriculum.cohorts.filter(active=True).filter(
#         suppress_card_generation=False
#     ):
#         for cohort_recruit in cohort.cohort_recruits.filter(user__active=True):
#             user = cohort_recruit.user
#             yield user


# def generate_all_content_cards(cohort):
#     for curriculum in helpers.get_curriculums(cohort):
#         print(f"processing curriculum: {curriculum}")
#         ordered_content_items = gen_helpers.get_ordered_content_items(curriculum)
#         for user in curriculum_users(curriculum):
#             print(f"processing user: {user}")

#             gen_helpers.create_or_update_content_cards_for_user(
#                 user, ordered_content_items
#             )
#         print()


# def generate_cards(cohort=None):
#     helpers.generate_project_cards(cohort, user=None)
#     # generate_topic_cards(cohort)
#     # generate_workshop_cards(cohort)
#     generate_all_content_cards(
#         cohort
#     )  # TODO, move this. most of the time that's not what we need
