from rest_framework import serializers
from dwitter.models import Comment, Dweet
from dwitter.templatetags.to_gravatar_url import to_gravatar_url
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')

    def get_avatar(self, obj):
        return to_gravatar_url(obj.email)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'posted',
            'reply_to',
            'author',
        )


class RemixOfSerializer(serializers.ModelSerializer):
    """ Dweet serializer for embedding dweets in the remix_of field """

    id = serializers.ReadOnlyField(source='pk')

    # Don't continue the chain of embedded remixes
    # and only include the ID of the next dweet
    remix_of = serializers.PrimaryKeyRelatedField(
        source='reply_to',
        queryset=Dweet.with_deleted.all()
    )

    awesome_count = serializers.SerializerMethodField()
    author = UserSerializer()

    class Meta:
        model = Dweet
        fields = (
            'author',
            'awesome_count',
            'code',
            'id',
            'posted',
            'remix_of',
        )

    def get_awesome_count(self, obj):
        return obj.likes.all().count()


class DweetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')

    remix_of = RemixOfSerializer(source='reply_to')

    awesome_count = serializers.SerializerMethodField()
    has_user_awesomed = serializers.SerializerMethodField()
    author = UserSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Dweet
        fields = (
            'author',
            'awesome_count',
            'code',
            'comments',
            'id',
            'posted',
            'remix_of',
            'has_user_awesomed',
        )

    def get_has_user_awesomed(self, dweet):
        user = self.context['request'].user
        return dweet.likes.filter(pk=user.pk).exists()

    def get_awesome_count(self, obj):
        return obj.likes.all().count()
