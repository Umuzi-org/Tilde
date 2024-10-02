import json
import re
from pathlib import Path
import os

from playwright.sync_api import sync_playwright, Page

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import F, Q

from curriculum_tracking.models import AgileCard, ContentItem, RecruitProjectReview
from curriculum_tracking.constants import RED_FLAG, NOT_YET_COMPETENT, COMPETENT
from taggit.models import Tag
from core.models import User
from backend.settings import (
    CURRICULUM_TRACKING_REVIEW_BOT_EMAIL,
    CURRICULUM_TRACKING_TRUSTED_REVIEW_BOT_EMAIL,
)


TODAY = timezone.now().date().strftime("%a %d %b %Y")

FREECODECAMP_AUTOMARKER_DATA_PATH = os.environ.get(
    "FREECODECAMP_AUTOMARKER_DATA_PATH", None
)

# MAPPING: dict[int, list[str]] = {
#         318: [
#         "Create a Basic JavaScript Object",
#         "Use Dot Notation to Access the Properties of an Object",
#         "Create a Method on an Object",
#         "Create a Method on an Object",
#         "Make Code More Reusable with the this Keyword",
#         "Define a Constructor Function",
#         "Use a Constructor to Create Objects",
#         "Extend Constructors to Receive Arguments",
#         "Verify an Object's Constructor with instanceof",
#         "Understand Own Properties",
#         "Use Prototype Properties to Reduce Duplicate Code",
#         "Iterate Over All Properties",
#         "Understand the Constructor Property",
#         "Change the Prototype to a New Object",
#         "Remember to Set the Constructor Property when Changing the Prototype",
#         "Understand Where an Object’s Prototype Comes From",
#         "Understand the Prototype Chain",
#         "Use Inheritance So You Don't Repeat Yourself",
#         "Inherit Behaviors from a Supertype",
#         "Set the Child's Prototype to an Instance of the Parent",
#         "Reset an Inherited Constructor Property",
#         "Add Methods After Inheritance",
#         "Override Inherited Methods",
#         "Use a Mixin to Add Common Behavior Between Unrelated Objects",
#         "Use Closure to Protect Properties Within an Object from Being Modified Externally",
#         "Understand the Immediately Invoked Function Expression (IIFE)",
#         "Use an IIFE to Create a Module",
#         "Set the Child's Prototype to an Instance of the Parent",
#         "Reset an Inherited Constructor Property",
#         "Add Methods After Inheritance",
#         "Override Inherited Methods",
#         "Use a Mixin to Add Common Behavior Between Unrelated Objects",
#         "Use Closure to Protect Properties Within an Object from Being Modified Externally",
#         "Understand the Immediately Invoked Function Expression (IIFE)",
#         "Use an IIFE to Create a Module",
#     ],
#     307: ,
# }


NYC_TEMPLATE = """Something has gone wrong - your timeline is missing some of the required items. Please make sure you have completed all required sections relevant to this project. You can click on __View Content__ on your project page to see the project instructions and requirements.

The missing items are:
- {missing_items}
"""
RED_FLAG_TEMPLATE = """Something has gone wrong - Your timeline is empty. Please make sure to set all your privacy settings to "Public"""


NEXT_BTN_SELECTOR = "ul.timeline-pagination_list button[aria-label='Go to next page']"


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.bot_user, _ = User.objects.get_or_create(
            email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL
        )
        self.trusted_bot_user, _ = User.objects.get_or_create(
            email=CURRICULUM_TRACKING_TRUSTED_REVIEW_BOT_EMAIL,
            is_superuser=True,
        )

        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

        self.handle_freecodecamp()

    def _get_automarker_data(self):
        with open(FREECODECAMP_AUTOMARKER_DATA_PATH, "r") as f:
            return json.load(f)

    def extract_timeline_from_page(self, page: Page, timeline):
        timeline_rows = page.query_selector_all(".timeline-row")
        for row in timeline_rows:
            title = row.query_selector("td a").inner_text()
            timeline.append(title)

    def handle_freecodecamp(self):
        freecodecamp_tag = Tag.objects.get(name="free-code-camp")
        freecodecamp_cards = (
            AgileCard.objects.filter(content_item__tags__in=[freecodecamp_tag])
            .filter(content_item__content_type=ContentItem.PROJECT)
            .filter(status=AgileCard.IN_REVIEW)
        )

        card_count = freecodecamp_cards.count()

        if not card_count:
            print("No cards to review")
            return

        automarker_data = self._get_automarker_data()
        available_content_item_ids = [i["content_item_id"] for i in automarker_data]

        with sync_playwright() as p:
            print(f"Starting review of {card_count} FreeCodeCamp projects")
            browser = p.firefox.launch(headless=True, timeout=60000)
            context = browser.new_context()
            page: Page = context.new_page()

            timeline = []

            for i, card in enumerate(freecodecamp_cards):
                project = card.recruit_project
                url = project.link_submission
                content_item_id = project.content_item.id

                page.goto(url)
                page.wait_for_selector(".bio-container")

                if content_item_id not in available_content_item_ids:
                    print(
                        f"Skipping {url} as there is no automarker data for content item {content_item_id}"
                    )
                    continue

                print(f"Reviewing {url} ({i+1}/{card_count})")

                while True:
                    self.extract_timeline_from_page(page, timeline)

                    next_page_btn = page.query_selector(NEXT_BTN_SELECTOR)
                    if not next_page_btn or not next_page_btn.is_visible():
                        break
                    next_page_btn.click()

                if not len(timeline):
                    self.add_review(
                        card,
                        RED_FLAG,
                        RED_FLAG_TEMPLATE,
                        self.bot_user,
                    )
                    continue

                required_items = next(
                    (
                        i["items"]
                        for i in automarker_data
                        if i["content_item_id"] == content_item_id
                    ),
                    [],
                )

                if not set(required_items).issubset(set(timeline)):
                    self.add_review(
                        card,
                        NOT_YET_COMPETENT,
                        NYC_TEMPLATE.format(
                            missing_items="\n- ".join(
                                list(set(required_items) - set(timeline))
                            )
                        ),
                        self.bot_user,
                    )
                    continue

                self.add_review(
                    card,
                    COMPETENT,
                    "Looks good. Well done on completing your project!",
                    self.bot_user,
                )

    def add_review(self, card, status, comments, bot_user):
        print(f"Adding review for card #{card.id} with status {status}")
        RecruitProjectReview.objects.create(
            status=status,
            timestamp=timezone.now(),
            comments=comments,
            recruit_project=card.recruit_project,
            reviewer_user=bot_user,
        )
