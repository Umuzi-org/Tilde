import json
import os

from playwright.sync_api import sync_playwright, Page

from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

from curriculum_tracking.models import AgileCard, ContentItem, RecruitProjectReview
from curriculum_tracking.constants import RED_FLAG, NOT_YET_COMPETENT, COMPETENT
from taggit.models import Tag
from core.models import User
from backend.settings import (
    CURRICULUM_TRACKING_REVIEW_BOT_EMAIL,
    CURRICULUM_TRACKING_TRUSTED_REVIEW_BOT_EMAIL,
)

FREECODECAMP_AUTOMARKER_DATA_PATH = os.environ.get(
    "FREECODECAMP_AUTOMARKER_DATA_PATH", None
)


NYC_TEMPLATE = """Something has gone wrong - your timeline is missing some of the required items. Please make sure you have completed all required sections relevant to this project. You can click on __View Content__ on your project page to see the project instructions and requirements.

The missing items are:
- {missing_items}
"""
RED_FLAG_TEMPLATE = """Something has gone wrong - We couldn't find your "timeline" on freecodecamp. Please make sure you have provided a valid link and all your privacy settings are set to "Public". """


NEXT_BTN_SELECTOR = "ul.timeline-pagination_list button[aria-label='Go to next page']"

FREECODECAMP_URL = "freecodecamp.org"
FREECODECAMP_TAG = "free-code-camp"


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.bot_user, _ = User.objects.get_or_create(
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

    @staticmethod
    def is_freecodecamp_url(url: str) -> bool:
        if not url:
            return False
        return FREECODECAMP_URL in url

    def handle_freecodecamp(self):
        automarker_data = self._get_automarker_data()
        available_content_item_ids = [i["content_item_id"] for i in automarker_data]

        freecodecamp_tag = Tag.objects.get(name=FREECODECAMP_TAG)
        freecodecamp_cards = (
            AgileCard.objects.filter(
                content_item__tags__in=[freecodecamp_tag],
                content_item__id__in=available_content_item_ids,
            )
            .filter(content_item__content_type=ContentItem.PROJECT)
            .filter(status=AgileCard.IN_REVIEW)
        )

        card_count = freecodecamp_cards.count()

        if not card_count:
            print("No cards to review")
            return

        with sync_playwright() as p:
            print(
                f"Starting review of {card_count} FreeCodeCamp projects as {self.bot_user.email}"
            )
            browser = p.firefox.launch(headless=True, timeout=60000)
            context = browser.new_context()
            page: Page = context.new_page()

            timeline = []

            for i, card in enumerate(freecodecamp_cards):
                print(f"Reviewing card #{card.id} ({i+1}/{card_count})")

                project = card.recruit_project
                url = project.link_submission
                content_item_id = project.content_item.id

                if not self.is_freecodecamp_url(url):
                    print(f"Red flagging {url}. Non freecodecamp project URL provided.")
                    self.add_review(card, RED_FLAG, RED_FLAG_TEMPLATE)
                    continue

                page.goto(url)
                page.wait_for_load_state()

                if page.query_selector("img[alt='404 Not Found:']"):
                    print(f"Red flagging {url}. Page not found.")
                    self.add_review(card, RED_FLAG, RED_FLAG_TEMPLATE)
                    continue

                page.wait_for_selector(".bio-container")

                while True:
                    self.extract_timeline_from_page(page, timeline)

                    next_page_btn = page.query_selector(NEXT_BTN_SELECTOR)
                    if not next_page_btn or not next_page_btn.is_visible():
                        break
                    next_page_btn.click()

                if not len(timeline):
                    self.add_review(card, RED_FLAG, RED_FLAG_TEMPLATE)
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
                    )
                    continue

                self.add_review(card, COMPETENT, "Well done!")

    def add_review(
        self,
        card,
        status,
        comments,
    ):
        bot_user = self.bot_user
        RecruitProjectReview.objects.create(
            status=status,
            timestamp=timezone.now(),
            comments=comments,
            recruit_project=card.recruit_project,
            reviewer_user=bot_user,
        )
        print(f"Added review for card #{card.id} with status {status}")
