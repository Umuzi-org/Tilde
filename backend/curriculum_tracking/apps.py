from django.apps import AppConfig


class CurriculumTrackingConfig(AppConfig):
    name = "curriculum_tracking"

    def ready(self):
        # register the signals
        import curriculum_tracking.signals
