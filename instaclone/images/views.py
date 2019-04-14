from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from instaclone.users.serializers import ListUserSerializer
from . import models, serializers
from notifications.views import create_notification
from instaclone.users import models as users_models
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class Feed(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, format=None):

        user = request.user
        following_users = user.following.all()
        image_list = []

        for following_user in following_users:
            user_images = following_user.images.all()[:2]
            for image in user_images:
                image_list.append(image)

        my_images = user.images.all()[:2]
        for image in my_images:
            image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)
        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)

class LikeImage(APIView):

    def get(self, request, image_id, format=None):

        likes = models.Like.objects.filter(image__id=image_id)
        like_creators = likes.values('creator_id')
        users = users_models.User.objects.filter(id__in=like_creators)
        serializer = ListUserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    def post(self, request, image_id, format=None):
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator=request.user,
                image=found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=request.user,
                image=found_image
            )

            create_notification(request.user, found_image.creator, 'like', found_image)
            return Response(status=status.HTTP_201_CREATED)

class UnlikeImage(APIView):

    def delete(self, request, image_id, format=None):

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator=request.user,
                image=found_image
            )
            preexisting_like.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)


        except models.Like.DoesNotExist:

            return Response(status=status.HTTP_304_NOT_MODIFIED)



class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=user, image=found_image)

            create_notification(user, found_image.creator,'comment', found_image, serializer.data['message'])


            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):

    def delete(self, request, comment_id, format=None):

        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class  Search(APIView):
    def get(self, request, format=None):
        hashtags = request.query_params.get('hashtags', None)

        if hashtags is not None:

            hashtags = list(map(lambda tag: tag.lower(), hashtags.split(',')))
            print(hashtags)
            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ModerateComment(APIView):

    def delete(self, request, image_id, comment_id, format=None):
        user = request.user

        try:
            comment_to_delete = models.Comment.objects.get(id=comment_id, image__id=image_id, image__creator=user)

        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comment_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageDetail(APIView):

    @staticmethod
    def find_own_image(image_id, user):
        try:
            image = models.Image.objects.get(id=image_id, creator=user)
            return image
        except models.Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):
        user = request.user

        try:
            image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ImageSerializer(image)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, image_id, format=None):
        user = request.user

        image = self.find_own_image(image_id, user)
        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, image_id, format=None):
        user = request.user

        image = self.find_own_image(image_id, user)
        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

