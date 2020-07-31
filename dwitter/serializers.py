from rest_framework import serializers
from django.utils.html import escape
from dwitter.models import Dweet, Comment, User
from dwitter.templatetags.insert_code_blocks import insert_code_blocks
from dwitter.templatetags.insert_magic_links import insert_magic_links
from dwitter.templatetags.to_gravatar_url import to_gravatar_url
from django.template.defaultfilters import urlizetrunc
from rest_framework_json_api import relations, serializers

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    author = relations.ResourceRelatedField(
        queryset=User.objects,
    )
    reply_to = relations.ResourceRelatedField(
        queryset=Comment.objects,
    )
    
    included_serializers = {
        'author': 'dwitter.serializers.UserSerializer',
        'reply_to': 'dwitter.serializers.DweetSerializer',
    }
    
    def get_created_at(self,obj):
        return obj.posted
        
    class JSONAPIMeta:
        included_resources = ['author','reply_to']

    class Meta:
        fields = ['author','created_at','reply_to','text']
        model = Comment

class DweetSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    is_deleted = serializers.SerializerMethodField()

    author = relations.ResourceRelatedField(
        queryset=User.objects,
    )
    comments = relations.ResourceRelatedField(
        queryset=Comment.objects,
        many=True,
    )
    reply_to = relations.ResourceRelatedField(
        queryset=Dweet.objects,
    )
    
    included_serializers = {
        'author': 'dwitter.serializers.UserSerializer',
        'comments': 'dwitter.serializers.CommentSerializer',
        'reply_to': 'dwitter.serializers.DweetSerializer',
    }
    
    def get_created_at(self,obj):
        return obj.posted
        
    def get_is_deleted(self,obj):
        return obj.deleted
    
    class JSONAPIMeta:
        included_resources = ['author','comments','reply_to']
    
    class Meta:
        fields = ['author','created_at','code','comments','is_deleted','reply_to']
        model = Dweet


class UserSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(format="%Y-%m-%d")
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'date_joined', 'link', 'avatar')

    def get_avatar(self, obj):
        return to_gravatar_url(obj.email)

    def get_link(self, obj):
        return 'https://www.dwitter.net/u/%s' % obj.username

'''
class CommentSerializer(serializers.ModelSerializer):
    urlized_text = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    posted = serializers.ReadOnlyField()
    reply_to = serializers.PrimaryKeyRelatedField(
        queryset=Dweet.with_deleted.all()
    )
    id = serializers.ReadOnlyField(source='pk')

    class Meta:
        model = Comment
        fields = ('id', 'urlized_text', 'text', 'posted', 'author', 'reply_to')

    def get_author(self, obj):
        return obj.author.username

    def get_urlized_text(self, obj):
        return insert_magic_links(
            urlizetrunc(
                insert_code_blocks(escape(obj.text)),
                45
            )
        )
'''


'''
class DweetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    remix_of = serializers.PrimaryKeyRelatedField(
        source='reply_to',
        queryset=Dweet.with_deleted.all()
    )
    link = serializers.SerializerMethodField()
    awesome_count = serializers.SerializerMethodField()
    author = UserSerializer()

    class Meta:
        model = Dweet
        fields = ('id', 'code', 'posted', 'author', 'link', 'awesome_count',
                  'remix_of')

    def get_awesome_count(self, obj):
        return obj.likes.all().count()

    def get_link(self, obj):
        return 'https://www.dwitter.net/d/%i' % obj.id
'''