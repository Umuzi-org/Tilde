from locust import HttpUser as LocustHttpUser
import logging


class HttpUser(LocustHttpUser):
    abstract = True

    def log_response(self, response):
        request = response.request

        logging.info(
            f"[{response.status_code}] {request.method} {request.url} {response.elapsed.total_seconds()}s"
        )

    def post(self, url, *args, **kwargs):
        response = self.client.post(url, *args, **kwargs)
        self.log_response(response)
        return response

    def get(self, url, *args, **kwargs):
        response = self.client.get(url, *args, **kwargs)
        self.log_response(response)
        return response
