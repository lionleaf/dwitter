from rest_framework import serializers
from dwitter.models import Dweet, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('pk', 'username')

class CommentSerializer(serializers.ModelSerializer):
  author = serializers.ReadOnlyField(source='author.username') 
  posted = serializers.ReadOnlyField()
  class Meta:
    model = Comment
    fields = ('text', 'posted', 'reply_to', 'author')

class DweetSerializer(serializers.ModelSerializer):
  latest_comments = serializers.SerializerMethodField()
  reply_to = serializers.PrimaryKeyRelatedField(queryset=Dweet.objects.all())

  class Meta:
    model = Dweet
    fields = ('pk', 'code', 'posted', 'author', 'likes','reply_to', 'latest_comments')

  def get_latest_comments(self, obj):
    cmnts = obj.comments.all().order_by('-posted')
    return CommentSerializer(cmnts[:3], many=True).data
    




