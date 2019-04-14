from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from notifications import serializers
from . import models

class Notifications(APIView):
    def get(self, request, format=None):
        user = request.user
        notifications = models.Notification.objects.filter(notification_to=user)
        serializer = serializers.notificationSerializer(notifications, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


def create_notification(notification_from, notification_to, notification_type, notification_image=None, notification_comment=None):

    notification = models.Notification.objects.create(
        notification_from=notification_from,
        notification_to=notification_to,
        notification_type=notification_type,
        notification_image=notification_image,
        notification_comment=notification_comment
    )

    notification.save()
