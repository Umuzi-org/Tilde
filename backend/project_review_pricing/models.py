from django.db import models
from curriculum_tracking.models import RecruitProjectReview, ContentItem
from model_mixins import FlavourMixin
from taggit.managers import TaggableManager
from .anthropic_interactions import (
    get_distinct_parts_from_review_comments,
    get_scores_from_comments,
)
from decimal import Decimal

reviewers = [  # TODO: put this somewhere better
    "raymond.mawina@umuzi.org",
    "aminat.amusa@umuzi.org",
    "mpho.mashau@umuzi.org",
    "themba.ntuli@umuzi.org",
    "ngoako.ramokgopa@umuzi.org",
    "percival.rapha@umuzi.org",
    "sbonelo.mkhize@umuzi.org",
    "vuyisanani.meteni@umuzi.org",
]


TRUSTED_REVIEW_MULTIPLIER = 1.5


class ProjectReviewPricingScore(models.Model):
    project_review = models.OneToOneField(
        RecruitProjectReview,
        related_name="price_score",
        on_delete=models.CASCADE,
    )
    score = models.SmallIntegerField(null=True, blank=True)

    weight_share = models.DecimalField(
        null=True, blank=True, decimal_places=3, max_digits=6
    )  # what weight is this worth? Total weight amount

    def __str__(self):
        review = self.project_review
        project = review.recruit_project
        return f"{review.reviewer_user.email} - {project.content_item.title} {project.flavour_names} - score:{self.score} weight:{self.weight}"

    @property
    def trust_adjusted_score(self):
        score = self.score
        if score < 0:
            score = 1
        if self.project_review.trusted:
            return score * TRUSTED_REVIEW_MULTIPLIER
        return score

    @classmethod
    def calculate_weight_shares_for_project(Cls, project):
        """Each project is worth a certain number of weight points (specified in ProjectReviewAgileWeight)

        Each review gets a score. Then the project weight is divided up between the reviews.
        """
        reviews = project.project_reviews.filter(reviewer_user__email__in=reviewers)

        review_scores = [
            ProjectReviewPricingScore.get_or_create_and_calculate_score(
                project_review=review
            )
            for review in reviews
        ]

        score_numbers = [o.trust_adjusted_score for o in review_scores]
        score_numbers = [i for i in score_numbers if i > 0]
        total_score = sum(score_numbers)

        weight_instance = ProjectReviewAgileWeight.get_review_weight(
            content_item_id=project.content_item_id, flavour_names=project.flavour_names
        )
        if not weight_instance:
            print(project)
            print(project.flavour_names)
            print([o.name for o in project.content_item.tags.all()])
            set_weight = int(input("What weight should this project have? (integer)"))
            weight_instance = ProjectReviewAgileWeight.set_review_weight(
                project.content_item_id, project.flavour_names, set_weight
            )
        total_weight = weight_instance.weight

        weight_per_score_point = (
            Decimal(total_weight) / Decimal(total_score) if total_score > 0 else 0
        )

        for score_instance in review_scores:
            score_instance.weight_share = weight_per_score_point * Decimal(
                score_instance.trust_adjusted_score
            )
            score_instance.save()

    @classmethod
    def get_or_create_and_calculate_score(Cls, project_review):
        instance, created = Cls.objects.get_or_create(project_review=project_review)

        if instance.score != None:
            return instance

        instance.calculate_score()
        return instance

    def calculate_score(self):
        """use ai to give the current review a score"""
        # TODO: check if this is like "looks good", in this case the score is 0

        parts = get_distinct_parts_from_review_comments(self.project_review.comments)

        part_scores = get_scores_from_comments(parts)
        self.score = sum(part_scores)
        self.save()


class ProjectReviewAgileWeight(models.Model, FlavourMixin):
    content_item = models.ForeignKey(ContentItem, on_delete=models.PROTECT)
    flavours = TaggableManager(blank=True)
    weight = models.SmallIntegerField()

    @classmethod
    def get_review_weight(Cls, content_item_id, flavour_names):
        l = Cls.objects.filter(content_item_id=content_item_id)
        for o in l:
            if o.flavours_match(flavour_names):
                return o

    @classmethod
    def set_review_weight(Cls, content_item_id, flavour_names, weight):
        o = Cls.get_review_weight(content_item_id, flavour_names)
        if o:
            o.weight = weight
            o.save()
            return o

        o = Cls.objects.create(content_item_id=content_item_id, weight=weight)
        o.set_flavours(flavour_names)
        return o
