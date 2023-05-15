# import logging

# from locust import between, task

# from grasshopper.lib.grasshopper import Grasshopper
# from grasshopper.lib.journeys.base_journey import BaseJourney
# from grasshopper.lib.util.utils import check

# logger = logging.getLogger(__name__)

# import os

# EMAIL = "challenger_0@email.com"


# class BackendForMiniFrontend(BaseJourney):
#     """An example journey class with a simple task"""

#     # number of seconds to wait between each task
#     wait_time = between(min_wait=10, max_wait=60)

#     host = os.environ["HOST_BACKEND_API"]

#     defaults = {}

#     def on_start(self):
#         METRIC = "POST login"
#         logger.info(f"Beginning {METRIC} task for VU {self.vu_number}")
#         response = self.client.post(
#             "/dj-rest-auth/login",
#             json={"username": EMAIL, "password": EMAIL},
#             name=METRIC,
#         )
#         logger.info(f"backend responded with a {response.status_code}.")

#     @task
#     def who_am_i(self):
#         METRIC = "GET who_am_i"
#         logger.info(f"Beginning {METRIC} task for VU {self.vu_number}")
#         response = self.client.get("/who_am_i/", name=METRIC, context={})
#         logger.info(f"backend responded with a {response.status_code}.")
#         check(
#             "api responded with a 200",
#             response.status_code == 200,
#             env=self.environment,
#         )


# def test_run_api_journey(complete_configuration):
#     BackendForMiniFrontend.update_incoming_scenario_args(complete_configuration)
#     locust_env = Grasshopper.launch_test(
#         BackendForMiniFrontend,
#         **complete_configuration,
#     )
#     return locust_env
