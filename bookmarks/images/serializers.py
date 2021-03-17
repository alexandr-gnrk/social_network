from rest_framework.serializers import ModelSerializer

from images.models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'user', 'title', 'slug', 'url', 'image', 'description', 'created', 'total_likes', 'users_like')
