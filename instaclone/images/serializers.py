from rest_framework import serializers

from instaclone.users.models import User
from . import models
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)



class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count',
        )



class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'profile_image',
        )



class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)
    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator',
        )



class LikeSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Like
        fields = '__all__'




class ImageSerializer(TaggitSerializer, serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer(read_only=True)
    tags = TagListSerializerField()
    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator',
            'tags'
        )

