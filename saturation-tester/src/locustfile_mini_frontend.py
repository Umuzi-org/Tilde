from locust import task
from env import HOST_FRONTEND_MINI

from helpers import HttpUser


class MiniFrontendUser(HttpUser):
    host = HOST_FRONTEND_MINI

    @task
    def visit_home_page(self):
        self.get("/")
