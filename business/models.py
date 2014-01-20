from django.db import models


class Neighborhood(models.Model):
    # This will need to be rethought..
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)


class Category(models.Model):
    # TODO: Nesting / Tree relationship
    name = models.CharField(max_length=100)


class Business(models.Model):
    business_yelp_slug = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    is_closed = models.BooleanField(default=False)

    address = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.ManyToManyField(Neighborhood)
    phone = models.IntegerField(blank=True, null=True)

    review_count = models.IntegerField(blank=True, null=True)  # Do I need this?
    display_stars = models.DecimalField(decimal_places=1, max_digits=2, blank=True, null=True)

    elite_count = models.IntegerField(blank=True, null=True)
    elite_stars = models.DecimalField(decimal_places=4, max_digits=5, blank=True, null=True)

    last_harvested = models.DateTimeField(auto_now=True)
