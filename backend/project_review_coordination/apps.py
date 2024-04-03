from django.apps import AppConfig


class ProjectReviewCoordinationConfig(AppConfig):
    name = 'project_review_coordination'

    def ready(self):
        import project_review_coordination.signals