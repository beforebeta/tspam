from django.contrib import admin
from inspiration.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Product, ProductAdmin)