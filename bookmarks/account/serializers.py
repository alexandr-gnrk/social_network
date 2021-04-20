from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from account.models import Profile
from actions.models import Action
from images.models import Image


class ActionProfileSerializer(ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'photo')


class ActionUserSerializer(ModelSerializer):
    profile = ActionProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'profile')


class ActionImageSerializer(ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'title', 'image')


class TargetRelatedField(serializers.RelatedField):
    """ A custom field to use for the `target` generic relationship.
    """
    def to_representation(self, value):
        """ Serialize image instances using a image serializer,
            and user instances using a user serializer.
        """
        if isinstance(value, Image):
            serializer = ActionImageSerializer(value)
        elif isinstance(value, User):
            serializer = ActionUserSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class ActionSerializer(ModelSerializer):
    user = ActionUserSerializer(read_only=True)
    target = TargetRelatedField(read_only=True)

    class Meta:
        model = Action
        fields = ('user', 'verb', 'target_ct', 'target_id', 'target', 'created')


class UserSerializer(ModelSerializer):
    profile = ActionProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'is_active', 'is_superuser', 'images_created', 'images_likes',
                  'following', 'followers', 'profile', 'stripe_id')


class UserFollowSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    id = serializers.IntegerField(required=True)
    action = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    """ Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User


class SendMailSerializer(serializers.Serializer):
    """ Serializer for sending mail to all users
    """
    subject = serializers.CharField(required=True)
    text = serializers.CharField(required=True)