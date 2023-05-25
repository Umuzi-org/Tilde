from locust import task, between
from env import HOST_AUTOMARKER
import time
import random
from helpers import HttpUser

ZMC_AUTOMARKER_CONFIG = [
    {"contentItemId": 866, "perfectProjectPath": "zmc_simple_website/first_site"},
    {"contentItemId": 869, "perfectProjectPath": "zmc_simple_website/adding_images"},
    {"contentItemId": 867, "perfectProjectPath": "zmc_simple_website/more_pages"},
    {"contentItemId": 871, "perfectProjectPath": "zmc_simple_website/intro_to_css"},
]

PASSING_PROJECT = "https://umuzi-org.github.io/zmc-first-website-automark-demo-site/"
FAILING_PROJECT = "https://sheenarbw.github.io/pres-app-engine-node/"

PROJECT_SUBMISSION_URLS = [PASSING_PROJECT, FAILING_PROJECT]


class AutomarkerUser(HttpUser):
    host = HOST_AUTOMARKER
    wait_time = between(120, 240)

    @task
    def mark_project(self):
        url = "/mark-project"
        project = random.choice(ZMC_AUTOMARKER_CONFIG)
        repoUrl = random.choice(PROJECT_SUBMISSION_URLS)
        self.post(
            url,
            json={
                "repoUrl": repoUrl,
                "contentItemId": project["contentItemId"],
                "flavours": [],
            },
        )
