from django.db import models

# Create your models here.

class Yelper(models.Model):
    yelp_id = models.CharField(primary_key=True, max_length=40)
    display_name = models.CharField(max_length=50)

    location = models.CharField(max_length=50, blank=True)
    yelping_since = models.CharField(max_length=20, blank=True)

    last_harvest = models.DateTimeField(null=True, blank=True)
    reviews = models.IntegerField(null=True, blank=True)

    elite = models.NullBooleanField()
