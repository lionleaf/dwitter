from rest_framework import serializers
from dwitter.models import Comment, Dweet
from dwitter.templatetags.to_gravatar_url import to_gravatar_url
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    # Confirmation password, only for validation
    password2 = serializers.CharField(allow_blank=False, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'password', 'password2', 'email')
        extra_kwargs = {
            'id': {'read_only': True},
            'avatar': {'read_only': True},
            'password': {'write_only': True},
            'password2': {'write_only': True},
            # email is not required in the database, so need to be set explicitly here
            'email': {'write_only': True, 'required': True,
                      'allow_null': False, 'allow_blank': False}
        }

    def validate(self, data):
        """
        Checks to be sure that the received password and password2 are the same
        And that the password meets auth.password_validation
        """
        errors = dict()
        try:
            # Note: 'password2' gets removed from the data here with pop
            if data['password'] != data.pop('password2'):
                errors['password'] = 'Passwords do not match'
            else:
                validate_password(data['password'])
        except ValidationError as e:
            errors['password'] = list(e.messages)

        # Any checks here only applies to the registration of new users
        if(data['username'] == '.' or data['username'] == '..'):
            # Since . and .. in urls can have special semantics in some cases (up directory)
            # best avoid them in usernames for new users
            errors['username'] = 'Invalid username'

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

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

    author = UserSerializer()

    class Meta:
        model = Dweet
        fields = (
            'author',
            'code',
            'id',
            'posted',
            'remix_of',
        )


class DweetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')

    remix_of = RemixOfSerializer(source='reply_to')
    remixes = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    awesome_count = serializers.IntegerField()
    has_user_awesomed = serializers.BooleanField()
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
            'remixes',
            'has_user_awesomed',
        )


