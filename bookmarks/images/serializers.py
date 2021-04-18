from urllib import request

from django.core.files.base import ContentFile
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from account.models import Profile
from actions.models import Action
from images.models import Image


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user', 'date_of_birth', 'photo')


class ImageSerializer(ModelSerializer):
    users_like = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)

    class Meta:
        model = Image
        fields = ('id', 'user', 'title', 'slug', 'url', 'image', 'description', 'created', 'total_likes', 'users_like')


class ImageDetailSerializer(ModelSerializer):
    # user.id -> user.username
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    users_like = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)
    # Extra field for context
    total_views = serializers.SerializerMethodField()
    users_like_photo = serializers.SerializerMethodField()

    def get_total_views(self, obj):
        if 'total_views' in self.context:
            return self.context['total_views']
        return None

    def get_users_like_photo(self, obj):
        if 'users_like_photo' in self.context:
            return self.context['users_like_photo']
        return None

    class Meta:
        model = Image
        fields = ('id', 'user', 'title', 'slug', 'url', 'image', 'description', 'created', 'total_likes', 'users_like',
                  'total_views', 'users_like_photo')


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
            # raise ValidationError('The given URL does not match valid image extensions.')
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
