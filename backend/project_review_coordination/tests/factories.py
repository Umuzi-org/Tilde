from factory.django import DjangoModelFactory
import factory

from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import RecruitProjectFactory

from project_review_coordination.models import ProjectReviewBundleClaim


class ProjectReviewBundleClaimFactory(DjangoModelFactory):
    class Meta:
        model = ProjectReviewBundleClaim

    claimed_by_user = factory.SubFactory(UserFactory)
    is_active = True

    @factory.post_generation
    def projects_to_review(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for project in extracted:
                self.projects_to_review.add(project)
        else:
            self.projects_to_review.add(RecruitProjectFactory())

    @factory.post_generation
    def projects_reviewed(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for project in extracted:
                self.projects_reviewed.add(project)
        else:
            self.projects_reviewed.add(RecruitProjectFactory())

    @factory.post_generation
    def projects_someone_else_got_to(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for project in extracted:
                self.projects_someone_else_got_to.add(project)
        else:
            self.projects_someone_else_got_to.add(RecruitProjectFactory())
