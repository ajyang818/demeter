from django.contrib import admin
from business.models import Business, Category, Neighborhood


class BusinessAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class NeighborhoodAdmin(admin.ModelAdmin):
    pass


admin.site.register(Business, BusinessAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)
