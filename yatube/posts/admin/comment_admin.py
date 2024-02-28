from django.contrib import admin
from django.contrib.admin import ModelAdmin

from ..models import Comment


class CommentAdmin(ModelAdmin):
    list_display = ('pk', 'post', 'author', 'text', 'created')
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Comment, CommentAdmin)
