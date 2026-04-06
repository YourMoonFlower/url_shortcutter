from django.contrib import admin

from .models import ClickModel, ShortURLModel


@admin.register(ClickModel)
class ClickAdmin(admin.ModelAdmin):
    pass


@admin.register(ShortURLModel)
class ShortURLAdmin(admin.ModelAdmin):
    pass
