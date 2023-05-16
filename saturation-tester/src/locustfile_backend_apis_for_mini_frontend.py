from locust import HttpUser, task, between, events
from env import HOST_BACKEND_API
import time
import random
import logging

STEP_INDEX_TOPIC = 0
STEP_INDEX_PROJECT = 4


def log_response(response):
    request = response.request

    logging.info(
        f"[{response.status_code}] {request.method} {request.url} {response.elapsed.total_seconds()}s"
    )


class BackendApiUser(HttpUser):
    host = HOST_BACKEND_API
    wait_time = between(60, 120)

    def on_start(self):
        response = self.client.post(
            "/dj-rest-auth/login/",
            json={
                "email": "challenger_0@email.com",
                "password": "challenger_0@email.com",
            },
        )
        log_response(response)

        self.token = response.json()["key"]

        self._who_am_i()
        self._get_active_challenges()

    def _who_am_i(self):
        response = self.client.get(
            "/who_am_i/",
            headers={"Authorization": f"Token {self.token}"},
        )
        log_response(response)
        # response.json looks like:
        # {'email': 'challenger_0@email.com', 'token': 'b51872a24357be34c08e1b4adbf94d8738b9ef09', 'user_id': 4, 'active': True, 'first_name': 'Daniel', 'last_name': 'Lawson', 'preferred_name': None, 'is_staff': 0, 'is_superuser': 0, 'permissions': {'teams': {}}}
        self.user_id = response.json()["user_id"]

    def _get_active_challenges(self):
        response = self.client.get(
            f"/challenge_registrations/?user={self.user_id}",
            headers={"Authorization": f"Token {self.token}"},
        )
        log_response(response)
        # logging.info(response.json())
        # [{'id': 1, 'user': 4, 'curriculum': 90, 'registration_date': '2023-04-17'}]
        self.challenge_registration_id = response.json()[0]["id"]

    def _get_challenge_details(self):
        url = f"/challenge_registrations/{self.challenge_registration_id}/"
        response = self.client.get(
            url,
            headers={"Authorization": f"Token {self.token}"},
        )
        log_response(response)

    def _start_step(self, step_index):
        response = self.client.post(
            f"/challenge_registrations/{self.challenge_registration_id}/start_step/",
            {"index": step_index},
            headers={"Authorization": f"Token {self.token}"},
        )
        log_response(response)

    def _finish_step(self, step_index):
        response = self.client.post(
            f"/challenge_registrations/{self.challenge_registration_id}/finish_step/",
            {"index": step_index},
            headers={"Authorization": f"Token {self.token}"},
        )
        log_response(response)

    def _get_step_details(self, step_index):
        response = self.client.get(
            f"/challenge_registrations/{self.challenge_registration_id}/step_details/?index={step_index}"
        )
        log_response(response)

    def _submit_project_link(self, step_index):
        url = f"/challenge_registrations/{self.challenge_registration_id}/submit_link/"
        response = self.client.post(
            url,
            {
                "index": step_index,
                "link_submission": "https://sheenarbw.github.io/pres-app-engine-node/",
            },
            headers={"Authorization": f"Token {self.token}"},
        )
        log_response(response)

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
