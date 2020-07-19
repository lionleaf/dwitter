from rest_framework import serializers
from dwitter.models import Comment, Dweet
from dwitter.templatetags.to_gravatar_url import to_gravatar_url
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        read_only_fields = ('id', 'username', 'avatar')
        fields = read_only_fields

    def get_avatar(self, obj):
        return to_gravatar_url(obj.email)

    def to_representation(self, instance):
        value = super().to_representation(instance)
        user = self.context['request'].user
        if user.is_authenticated and user.id == instance.id:
            value['email'] = user.email
        return value


class SetEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class SetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise ValidationError('Wrong password.')
        return old_password

    def validate_new_password(self, new_password):
        validate_password(new_password)
        return new_password

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


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
