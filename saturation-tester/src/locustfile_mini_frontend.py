from locust import HttpUser, task
from env import HOST_FRONTEND_MINI


class MiniFrontendUser(HttpUser):
    host = HOST_FRONTEND_MINI

    @task
    def visit_home_page(self):
        self.client.get("/")
