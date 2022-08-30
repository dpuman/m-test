from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Variant)
class FounderAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class FounderAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class FounderAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductVariant)
class FounderAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductVariantPrice)
class FounderAdmin(admin.ModelAdmin):
    pass
