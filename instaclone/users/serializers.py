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

    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    post_count = serializers.ReadOnlyField()


    class Meta:
        model = models.User
        fields = (
            'id',
            'website',
            'bio',
            'profile_image',
            'username',
            'name',
            'post_count',
            'following_count',
            'followers_count',
            'images'
        )
