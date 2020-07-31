from dwitter.models import Dweet, Comment, Hashtag, User
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
    remix_of = relations.ResourceRelatedField(
        queryset=Dweet.objects
    )
    
    included_serializers = {
        'author': 'dwitter.serializers.UserSerializer',
        'comments': 'dwitter.serializers.CommentSerializer',
        'remix_of': 'dwitter.serializers.DweetSerializer',
    }
    
    def get_created_at(self,obj):
        return obj.posted
        
    def get_is_deleted(self,obj):
        return obj.deleted
    
    class JSONAPIMeta:
        included_resources = ['author','comments','remix_of']
    
    class Meta:
        fields = ['author','created_at','code','comments','is_deleted','remix_of']
        model = Dweet


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name']
        model = Hashtag

class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    
    def get_created_at(self,obj):
        return obj.date_joined
    
    def get_avatar_url(self, obj):
        return obj.get_avatar_url()

    class Meta:
        fields = ['username', 'created_at','avatar_url','is_staff']
        model = User