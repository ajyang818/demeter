from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Neighborhood(models.Model):
    # This will need to be rethought..
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)


class Category(MPTTModel):
    slug = models.SlugField(primary_key=True, max_length=200)
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


class Business(models.Model):
    business_yelp_slug = models.SlugField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    is_closed = models.BooleanField(default=False)

    address = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.ManyToManyField(Neighborhood)
    phone = models.IntegerField(blank=True, null=True)

    review_count = models.IntegerField(blank=True, null=True)  # Do I need this?
    stars = models.DecimalField(decimal_places=1, max_digits=2, blank=True, null=True)

    elite_count = models.IntegerField(blank=True, null=True)
    elite_stars = models.DecimalField(decimal_places=4, max_digits=5, blank=True, null=True)

    last_harvested = models.DateTimeField(auto_now=True)
