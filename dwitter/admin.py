from django.contrib import admin
from .models import Comment
from .models import Dweet


class DweetAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'reply_to', 'likes',)


class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'reply_to',)


admin.site.register(Dweet, DweetAdmin)
admin.site.register(Comment, CommentAdmin)
