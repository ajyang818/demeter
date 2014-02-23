import csv

from business.models import Category

INPUT_FILE = 'business/data/all_yelp_categories.csv'


def import_yelp_cats():
    ff = open(INPUT_FILE, 'U')
    reader = csv.reader(ff)

    for row in reader:
        parent = row[0]
        combo = row[1]

        name = combo[:(combo.find('(')-1)]
        slug = combo[(combo.find('(')+1):combo.find(')')]

        parent_obj = Category.objects.get(slug=parent) if parent != '' else None
        try:
            Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            Category.objects.create(slug=slug, name=name, parent=parent_obj)
