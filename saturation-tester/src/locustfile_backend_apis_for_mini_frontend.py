from locust import task, between, events
from env import HOST_BACKEND_API
import time
import random
import logging
from helpers import HttpUser


STEP_INDEX_TOPIC = 0
STEP_INDEX_PROJECT = 4


class BackendApiUser(HttpUser):
    host = HOST_BACKEND_API
    wait_time = between(60, 120)

    def on_start(self):
        response = self.post(
            "/dj-rest-auth/login/",
            json={
                "email": "challenger_0@email.com",
                "password": "challenger_0@email.com",
            },
        )
        self.token = response.json()["key"]

        self._who_am_i()
        self._get_active_challenges()

    def _who_am_i(self):
        response = self.get(
            "/zmc/who_am_i/",
            headers={"Authorization": f"Token {self.token}"},
        )
        self.user_id = response.json()["user_id"]

    def _get_active_challenges(self):
        response = self.get(
            f"/challenge_registrations/?user={self.user_id}",
            headers={"Authorization": f"Token {self.token}"},
        )
        self.challenge_registration_id = response.json()[0]["id"]

    def _get_challenge_details(self):
        url = f"/challenge_registrations/{self.challenge_registration_id}/"
        self.get(
            url,
            headers={"Authorization": f"Token {self.token}"},
        )

    def _start_step(self, step_index):
        self.post(
            f"/challenge_registrations/{self.challenge_registration_id}/start_step/",
            {"index": step_index},
            headers={"Authorization": f"Token {self.token}"},
        )

    def _finish_step(self, step_index):
        self.post(
            f"/challenge_registrations/{self.challenge_registration_id}/finish_step/",
            {"index": step_index},
            headers={"Authorization": f"Token {self.token}"},
        )

    def _get_step_details(self, step_index):
        self.get(
            f"/challenge_registrations/{self.challenge_registration_id}/step_details/?index={step_index}"
        )

    def _submit_project_link(self, step_index):
        url = f"/challenge_registrations/{self.challenge_registration_id}/submit_link/"
        self.post(
            url,
            {
                "index": step_index,
                "link_submission": "https://sheenarbw.github.io/pres-app-engine-node/",
            },
            headers={"Authorization": f"Token {self.token}"},
        )

    @task
    def visit_challenge_page(self):
        self._who_am_i()
        self._get_challenge_details()

    @task
    def visit_topic_step_page(self):
        self._who_am_i()
        self._get_challenge_details()
        self._start_step(STEP_INDEX_TOPIC)
        self._get_step_details(STEP_INDEX_TOPIC)

        time.sleep(random.randrange(3 * 60, 8 * 60))

        self._finish_step(STEP_INDEX_TOPIC)

    @task
    def visit_project_step_page(self):
        self._who_am_i()
        self._get_challenge_details()
        self._start_step(STEP_INDEX_PROJECT)
        self._get_step_details(STEP_INDEX_PROJECT)

        for _ in range(int(random.random() * 3)):
            time.sleep(
                random.randrange(5 * 60, 10 * 60)
            )  # 5-10 minutes. probably unrealisticly short

            self._submit_project_link(STEP_INDEX_PROJECT)

            for _ in range(int(random.random() * 10)):
                self._get_step_details(STEP_INDEX_PROJECT)
                time.sleep(5)


@events.quitting.add_listener
def _(environment, **kw):
    MAX_AVG_RESPONSE_TIME = 1000
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > MAX_AVG_RESPONSE_TIME:
        logging.error(
            f"Test failed due to average response time ratio > {MAX_AVG_RESPONSE_TIME} ms"
        )
        environment.process_exit_code = 1
    # elif environment.stats.total.get_response_time_percentile(0.95) > 800:
    #     logging.error("Test failed due to 95th percentile response time > 800 ms")
    #     environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0
