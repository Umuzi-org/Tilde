from django.core.management.base import BaseCommand

from curriculum_tracking.models import AgileCard, ContentItem, RecruitProjectReview
from curriculum_tracking.constants import RED_FLAG, NOT_YET_COMPETENT, COMPETENT
from taggit.models import Tag
from core.models import User
from django.utils import timezone

from googleapiclient.discovery import build
from google_helpers.utils import authorize_creds
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import json
import re
from pathlib import Path

from backend.settings import CURRICULUM_TRACKING_REVIEW_BOT_EMAIL

DESTINATION = Path("gitignore/ncit_downloads")
TODAY = timezone.now().date().strftime("%a %d %b %Y")


class Command(BaseCommand):
    def handle(self, *args, **options):
        credentials = authorize_creds()
        service = build("drive", "v3", credentials=credentials)

        self.bot_user, _ = User.objects.get_or_create(
            email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL
        )
        ncit_tag = Tag.objects.get(name="ncit")
        all_cards = AgileCard.objects.filter(content_item__tags__in=[ncit_tag]).filter(
            content_item__content_type=ContentItem.PROJECT
        )

        cards_in_review = all_cards.filter(status=AgileCard.IN_REVIEW)
        for card in cards_in_review:
            url = card.recruit_project.link_submission
            if url:
                if url.startswith("https://drive.google.com/"):
                    self.sync_card_drive_link(card, service)
                elif url.startswith("https://docs.google.com/"):
                    self.sync_card_drive_link(card, service)
                else:
                    # print(f"skipping: {url}")
                    # continue

                    self.add_review(
                        card,
                        NOT_YET_COMPETENT,
                        "Please follow the submission instructions exactly: Upload the document to google drive and submit a link",
                    )
            else:
                self.add_review(
                    card,
                    RED_FLAG,
                    "Please submit a link to your work before asking for a review. Make sure your work is publically accessable so it can be reviewed",
                )

    # def sync_card_docs_link(self, card):
    #     user: User = card.assignees.first()
    #     link = card.recruit_project.link_submission
    #     print(f"processing link:\n\t{link}")

    #     credentials = authorize_creds()
    #     service = build("drive", "v3", credentials=credentials)
    #     breakpoint()
    #     pass

    def sync_card_drive_link(self, card, service):

        user: User = card.assignees.first()
        link = card.recruit_project.link_submission
        print(f"processing link:\n\t{link}")

        extension = (
            "docx"  # If we ever support other file types then this will stop working
        )
        filename = f"{user.last_name} {user.first_name} [{user.id}] {card.content_item.title} {TODAY}.{extension}"
        file_path = DESTINATION / filename

        if file_path.exists():
            print("already downloaded")
            return

        import time

        time.sleep(10)

        found = re.search("https://drive.google.com/file/d/(.*)/", link) or re.search(
            "https://docs.google.com/document/d/(.*)/", link
        )
        if found:
            file_id = found.groups()[0]
        else:
            self.add_review(
                card,
                RED_FLAG,
                "This link is not valid. Please link to a specific file in your google drive. The link should look like this: https://docs.google.com/file/d/SOME_WEIRD_STUFF/...",
            )
            return

        try:
            metadata = service.files().get(fileId=file_id).execute()
        except HttpError as e:
            if json.loads(e.content)["error"]["code"] == 404:

                self.add_review(
                    card,
                    RED_FLAG,
                    "This link is not accessable. Please make sure it points to something that exists. The file needs to be publically accessable so that it can be reviewed. Try opening your own link in an incognito window, it should work",
                )
                return
        has_extension = len(metadata["name"].split(".")) > 1
        if not has_extension:
            self.add_review(
                card,
                NOT_YET_COMPETENT,
                "Something has gone wrong - your file was meant to have a .docx extension, but it doesn't. Are you sure you submitted the right file type?",
            )
            return
        extension = metadata["name"].split(".")[-1]
        if extension not in ["docx"]:
            self.add_review(
                card,
                NOT_YET_COMPETENT,
                "Something has gone wrong - your file was meant to have a .docx extension, but it doesn't. Are you sure you submitted the right file type?",
            )
            return

        request = service.files().get_media(fileId=file_id)

        with open(file_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                try:
                    status, done = downloader.next_chunk()
                except HttpError as e:
                    if json.loads(e.content)["error"]["code"] == 403:
                        self.add_review(
                            card,
                            RED_FLAG,
                            "There is something wrong with your file. Please try again. Make sure that you\n- created a docx file on your local computer\n- uploaded the file to google drive\n- made the file public\n- gave us the correct link",
                        )
                        return
                    else:
                        raise

                # print("Download %d%%." % int(status.progress() * 100))

        has_review = (
            card.recruit_project.project_reviews.filter(
                timestamp__gt=card.recruit_project.review_request_time
            )
            .filter(reviewer_user=self.bot_user)
            .count()
        )

        if not has_review:
            self.add_review(
                card,
                COMPETENT,
                "The link works. This project is ready for assessment",
            )

    def add_review(self, card, status, comments):
        review = RecruitProjectReview.objects.create(
            status=status,
            timestamp=timezone.now(),
            comments=comments,
            recruit_project=card.recruit_project,
            reviewer_user=self.bot_user,
        )


# url = (
#     "https://drive.google.com/file/d/1MWkJNh8uyhIUe4PteNohH1HYuocRiE5Q/view?usp=sharing"
# )
# file_id = "1MWkJNh8uyhIUe4PteNohH1HYuocRiE5Q"


# url = "https://drive.google.com/file/d/1-Tqi3WZKwu8H3fK2AVJ9gvc8e0a0czOC/view"  # ok
# file_id = "1-Tqi3WZKwu8H3fK2AVJ9gvc8e0a0czOC"


# request = service.files().get_media(fileId=file_id)


# with open("gitignore/temp2.docx", "wb") as fh:
#     downloader = MediaIoBaseDownload(fh, request)
#     done = False
#     while done is False:
#         try:
#             status, done = downloader.next_chunk()
#         except HttpError as e:
#             # error['e'] = e
#             done = True
#             print(json.loads(e.content)["error"]["code"] == 404)
#         else:
#             print("Download %d%%." % int(status.progress() * 100))
