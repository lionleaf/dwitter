from django.contrib import admin
from dwitter.models import Comment, Dweet, Hashtag, User


class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'reply_to',)


class DweetAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'reply_to', 'likes',)


class HashtagAdmin(admin.ModelAdmin):
    raw_id_fields = ()


class UserAdmin(admin.ModelAdmin):
    raw_id_fields = ()


admin.site.register(Comment, CommentAdmin)
admin.site.register(Dweet, DweetAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(User, UserAdmin)
