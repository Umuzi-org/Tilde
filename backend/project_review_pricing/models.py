from django.db import models
from curriculum_tracking.models import RecruitProjectReview, ContentItem
from model_mixins import FlavourMixin
from taggit.managers import TaggableManager
from .anthropic_interactions import (
    get_distinct_parts_from_review_comments,
    get_scores_from_comments,
)


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


class ProjectReviewPricingScore(models.Model):
    project_review = models.OneToOneField(
        RecruitProjectReview,
        related_name="price_score",
        on_delete=models.CASCADE,
    )
    score = models.SmallIntegerField(null=True, blank=True)

    weight_share = models.FloatField(
        null=True, blank=True
    )  # what weight is this worth? Total weight

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
    def get_review_weight(Cls,content_item_id,flavour_names):
        l = Cls.objects.filter(content_item_id=content_item_id)
        for o in l: 
            if o.flavours_match(flavour_names):
                return o 

    @classmethod
    def set_review_weight(Cls,content_item_id,flavour_names,weight):    
        o = Cls.get_review_weight( content_item_id, flavour_names)
        if o: 
            o.weight = weight
            o.save() 
            return 
            
        o = Cls.objects.create(content_item_id=content_item_id, weight=weight)
        o.set_flavours(flavour_names)