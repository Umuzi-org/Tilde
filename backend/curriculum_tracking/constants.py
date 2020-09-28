import os
from pathlib import Path

CLONE_DESTINATION = Path(
    os.environ.get("CURRICULUM_CLONE_DIR", "gitignore/sync_curriculum")
)
REPO_SSH_URL = "git@github.com:Umuzi-org/tech-department.git"
REPO_NAME = "tech-department"


FULL_PATH = CLONE_DESTINATION / REPO_NAME
CURRICULUMS_BASE_DIR = FULL_PATH / "content/syllabuses"

RAW_CONTENT_URL = "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/{content_sub_dir}"


CURRICULUM_STATIC_SITE_URL = "https://umuzi-org.github.io/tech-department/"


NOT_YET_COMPETENT = "NYC"
COMPETENT = "C"
EXCELLENT = "E"
RED_FLAG = "R"

REVIEW_STATUS_CHOICES = [
    (NOT_YET_COMPETENT, "not yet competent"),
    (COMPETENT, "competent"),
    (EXCELLENT, "excellent"),
    (RED_FLAG, "red flag"),
]

