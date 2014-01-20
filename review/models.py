from django.db import models

from yelper.models import Yelper
from business.models import Business


class Review(models.Model):
    review_yelp_id = models.CharField(primary_key=True, max_length=40)

    yelper = models.ForeignKey(Yelper)
    business = models.ForeignKey(Business)

    publish_date = models.DateTimeField()
    harvest_date = models.DateTimeField(auto_now=True)
    stars = models.DecimalField(decimal_places=1, max_digits=2)

    review_text = models.CharField(max_length=5250)

    rotd = models.BooleanField(default=False)
    updated_review = models.BooleanField(default=False)
    # How to handle old review? Discarding for now
    # TODO: Link an old review to an update
