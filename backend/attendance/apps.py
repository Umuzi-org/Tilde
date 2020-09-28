from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    name = 'attendance'

    def ready(self):
        # register the signals
        import attendance.signals
