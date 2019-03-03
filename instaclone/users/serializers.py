from rest_framework import serializers
from . import models
from instaclone.images import serializers as image_serializers


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name',
        )




class UserProfileSerializer(serializers.ModelSerializer):

    images = image_serializers.CountImageSerializer(many=True)

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name',
            'post_count',
            'following_count',
            'followers_count',
            'images'
        )
