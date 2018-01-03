from rest_framework import serializers
from dwitter.models import Dweet, Comment
from dwitter.templatetags.insert_magic_links import insert_magic_links
from django.contrib.auth.models import User
from django.template.defaultfilters import urlizetrunc


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    posted = serializers.ReadOnlyField()
    urlized_text = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('urlized_text', 'text', 'posted', 'reply_to', 'author')

    def get_urlized_text(self, obj):
        return insert_magic_links(urlizetrunc(obj.text, 45))


class DweetSerializer(serializers.ModelSerializer):
    latest_comments = serializers.SerializerMethodField()
    reply_to = serializers.PrimaryKeyRelatedField(
        queryset=Dweet.with_deleted.all()
    )

    class Meta:
        model = Dweet
        fields = ('pk', 'code', 'posted', 'author',
                  'likes', 'reply_to', 'latest_comments')

    def get_latest_comments(self, obj):
        cmnts = obj.comments.all().order_by('-posted')
        return CommentSerializer(cmnts[:3], many=True).data
