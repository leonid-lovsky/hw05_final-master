from django.contrib import admin
from django.contrib.admin import ModelAdmin

from ..models import Group


class GroupAdmin(ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title', 'description')
    empty_value_display = '-пусто-'


admin.site.register(Group, GroupAdmin)
