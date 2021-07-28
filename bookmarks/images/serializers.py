from urllib import request

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from account.models import Profile
from images.models import Image


class UserLikeProfileSerializer(ModelSerializer):
    # user.id -> user.username
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'photo')


class UserLikeSerializer(ModelSerializer):
    profile = UserLikeProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'following', 'profile')


class ImageSerializer(ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # users_like = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)
    users_like = UserLikeSerializer(many=True, read_only=True)
    # Extra field for context
    total_views = serializers.SerializerMethodField()

    def get_total_views(self, obj):
        if 'total_views' in self.context:
            return self.context['total_views']
        return None

    class Meta:
        model = Image
        fields = ('id', 'user', 'title', 'slug', 'url', 'image', 'description', 'created', 'total_likes', 'users_like',
                  'total_views')


class ImageCreateSerializer(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Image
        fields = ('user', 'title', 'url', 'description')

    def clean_url(self):
        url = self.validated_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if not extension in valid_extensions:
            return Response('The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save()
        image_url = image.url
        image_name = '{}.{}'.format(
            slugify(image.title),
            image_url.rsplit('.', 1)[1].lower())
        # Download an image from url
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        image.save()
        return image


class ImageRankingSerializer(ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'title', 'image')


class ImageLikeSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    id = serializers.IntegerField(required=True)
    action = serializers.CharField(required=True)
