from rest_framework import  serializers
from . import  models
from instaclone.users import serializers as users_serializers
from instaclone.images import serializers as models_serializers

class notificationSerializer(serializers.ModelSerializer):

    notification_from = users_serializers.ListUserSerializer()
    notification_image = models_serializers.SmallImageSerializer()

    class Meta:
        model = models.Notification
        fields = '__all__'
