import factory
from django.contrib.auth.models import User
from account.models import Profile, Contact
from images.models import Image


# new user creation with Factory boy
class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

class ProfileFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Profile

	user = factory.SubFactory(UserFactory)

class ImageFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Image