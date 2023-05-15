import logging

from locust import between, task

from grasshopper.lib.grasshopper import Grasshopper
from grasshopper.lib.journeys.base_journey import BaseJourney
from grasshopper.lib.util.utils import check

logger = logging.getLogger(__name__)

import os


class MiniFrontendGetHome(BaseJourney):
    """An example journey class with a simple task"""

    # number of seconds to wait between each task
    wait_time = between(min_wait=1, max_wait=4)

    # `host` is automatically prepended to all request endpoint
    # urls when using `self.client` requests. It is also set as the
    # global "environment" tag in timeseries metrics
    # host = "https://google.com"
    host = os.environ["HOST_FRONTEND_MINI"]

    # lower precedence scenario_args dict, merged in on startup
    defaults = {
        # "foo": "bar",
    }

    # a locust task, repeated over and over again until the test finishes
    @task
    def get_home_page(self):
        """a simple get home page HTTP request"""
        logger.info(f"Beginning get_home_page task for VU {self.vu_number}")
        # aggregate all metrics for this request under the name "get home page"
        # if name is not specified, then the full url will be the name of the metric
        response = self.client.get("/", name="get home page", context={})
        logger.info(f"frontend responded with a {response.status_code}.")
        check(
            "frontend responded with a 200",
            response.status_code == 200,
            env=self.environment,
        )


def test_run_example_journey(complete_configuration):
    here
    MiniFrontendGetHome.update_incoming_scenario_args(complete_configuration)
    locust_env = Grasshopper.launch_test(
        MiniFrontendGetHome,
        **complete_configuration,
    )
    return locust_env
