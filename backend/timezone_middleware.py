import zoneinfo
from django.utils import timezone

class TimezoneMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_tz = request.COOKIES.get("tilde_tz")
        if user_tz:
            timezone.activate(zoneinfo.ZoneInfo(user_tz))
        else:
            timezone.activate(zoneinfo.ZoneInfo("Africa/Johannesburg"))
        return self.get_response(request)