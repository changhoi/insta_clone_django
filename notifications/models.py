from django.db import models
# Create your models here.
from instaclone.users import models as user_models
from instaclone.images import models as images_models

class Notification(images_models.TimeStampedModel):
    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )

    notification_from = models.ForeignKey(user_models.User, related_name='creator', on_delete=models.CASCADE)
    notification_to = models.ForeignKey(user_models.User, related_name='to', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    notification_image = models.ForeignKey(images_models.Image, null=True, blank=True, on_delete=models.CASCADE)
    notification_comment = models.TextField(null=True, blank=True)
