from locust import HttpUser, task, between
from env import HOST_BACKEND

# generate using https://github.com/SvenskaSpel/har2locust


class BackendApiUser(HttpUser):
    host = HOST_BACKEND
    wait_time = between(1, 10)

    # @task
    # def hello_world(self):
    #     self.client.get("/")

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})
