from google.cloud import error_reporting
import logging
import sys
import traceback
import os

GOOGLE_CLOUD_ERROR_REPORTING = int(os.environ.get("GOOGLE_CLOUD_ERROR_REPORTING", 0))


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):

        exc_type, exc_value, exc_traceback = sys.exc_info()

        error = "\n".join(
            [
                s.strip("\n")
                for s in traceback.format_exception(exc_type, exc_value, exc_traceback)
            ]
        )

        logger = logging.getLogger("django")

        logger.error(error)

        if GOOGLE_CLOUD_ERROR_REPORTING:
            try:
                raise exception
            except:

                # logger.error(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
                # with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], "r") as f:
                #     logger.error(f.read(20))

                client = error_reporting.Client()
                client.report(error)
                # client.report_exception(exception)
