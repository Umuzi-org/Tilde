import traceback
import logging

logger = logging.getLogger(__name__)


class RequestUserLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = "anonomous"

        verb = request.method
        url = request.get_full_path()

        logger.info(f"{email} [{verb}] {url}")

        return self.get_response(request)
