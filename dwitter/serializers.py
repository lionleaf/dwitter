from dwitter.models import Dweet, Comment, Hashtag, User
from rest_framework_json_api import relations, serializers


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    author = relations.ResourceRelatedField(
        queryset=User.objects,
        related_link_view_name='comment-related',
        self_link_view_name='comment-relationships',
    )
    reply_to = relations.ResourceRelatedField(
        queryset=Comment.objects,
        related_link_view_name='comment-related',
        self_link_view_name='comment-relationships',
    )

    included_serializers = {
        'author': 'dwitter.serializers.UserSerializer',
        'reply_to': 'dwitter.serializers.DweetSerializer',
    }

    def get_created_at(self, obj):
        return obj.posted

    class JSONAPIMeta:
        included_resources = ['author', 'reply_to']

    class Meta:
        fields = ['author', 'created_at', 'reply_to', 'text']
        model = Comment


class DweetSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    is_deleted = serializers.SerializerMethodField()

    author = relations.ResourceRelatedField(
        queryset=User.objects,
        related_link_view_name='dweet-related',
        self_link_view_name='dweet-relationships',
    )
    comments = relations.ResourceRelatedField(
        many=True,
        queryset=Comment.objects,
        related_link_view_name='dweet-related',
        self_link_view_name='dweet-relationships',
    )

    remix_of = relations.SerializerMethodResourceRelatedField(
        queryset=Dweet.objects,
        related_link_view_name='dweet-related',
        default=False,
        self_link_view_name='dweet-relationships',
        source='reply_to',
    )

    included_serializers = {
        'author': 'dwitter.serializers.UserSerializer',
        'comments': 'dwitter.serializers.CommentSerializer',
        'remix_of': 'dwitter.serializers.DweetSerializer',
    }

    def get_created_at(self, obj):
        return obj.posted

    def get_is_deleted(self, obj):
        return obj.deleted

    class JSONAPIMeta:
        included_resources = ['author', 'comments', 'remix_of']

    class Meta:
        fields = ['author', 'created_at', 'code', 'comments', 'is_deleted', 'remix_of']
        model = Dweet


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name']
        model = Hashtag


class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.date_joined

    def get_avatar_url(self, obj):
        return obj.get_avatar_url()

    class Meta:
        fields = ['username', 'created_at', 'avatar_url', 'is_staff']
        model = User
