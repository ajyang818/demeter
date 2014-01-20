from django.contrib import admin
from yelper.models import Yelper


class YelperAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'location', 'reviews', 'last_harvest')


admin.site.register(Yelper, YelperAdmin)
