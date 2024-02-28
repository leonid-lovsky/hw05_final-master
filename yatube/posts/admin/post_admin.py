from django.contrib import admin
from django.contrib.admin import ModelAdmin

from ..models import Post


class PostAdmin(ModelAdmin):
    list_display = ('pk', 'text', 'author', 'group', 'image', 'pub_date')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
