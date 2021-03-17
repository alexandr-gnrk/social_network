from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q
from account.models import Profile
from actions.utils import create_action
from account.forms import UserRegistrationForm


class RegisterSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'email', 'password', 'password2']
		extra_kwargs = {'password': {'write_only': True}}

	def validate_email(self, value):
		user = User.objects.filter(email__iexact=value)
		if user.exists():
			raise serializers.ValidationError("A user with that email already exists.")
		return value

	def validate(self, data):
		pw 	= data['password']
		pw2 = data.pop('password2')
		if pw2 != pw:
			raise serializers.ValidationError('Passwords must match')
		return data

	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'], 
			email=validated_data['email'], 
			first_name=validated_data['first_name']
		)
		user.set_password(validated_data['password'])
		user.save()
		Profile.objects.create(user=user)
		create_action(user, 'has created an account')
		return user


class ChangePasswordSerializer(serializers.Serializer):
	""" Serializer for password change endpoint.
	"""
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)

	class Meta:
		model = User






