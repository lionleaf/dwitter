from rest_framework import serializers
from dwitter.models import Dweet, Comment
from dwitter.templatetags.insert_magic_links import insert_magic_links
from django.contrib.auth.models import User
from django.template.defaultfilters import urlizetrunc


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.ReadOnlyField(source='pk')
        model = User
        fields = ('id', 'username')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    urlized_text = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('pk', 'urlized_text', 'text', 'posted', 'reply_to', 'author')

    def get_urlized_text(self, obj):
        return insert_magic_links(urlizetrunc(obj.text, 45))


class DweetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    remix_of = serializers.PrimaryKeyRelatedField(
        source='reply_to',
        queryset=Dweet.with_deleted.all()
    )
    awesome_count = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Dweet
        fields = ('id', 'code', 'posted', 'author', 'author_name', 'awesome_count',
                  'remix_of')

    def get_author_name(self, obj):
        return obj.author.username

    def get_awesome_count(self, obj):
        return obj.likes.all().count()
