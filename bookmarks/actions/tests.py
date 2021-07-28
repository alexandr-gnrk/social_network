from django.test import TestCase
import unittest
from actions import utils
from account.models import Profile
from actions.test.factories import (
	UserFactory, 
	ProfileFactory,
	ImageFactory,
)
from account.models import Contact


class ActionsTestCase(unittest.TestCase):
	def test_profile_create_action(self):
		new_user = UserFactory.create(username='John', password='Uytrewq123')
		ProfileFactory(user=new_user)

		#utils.create_action returns True if profile has been created
		result = utils.create_action(new_user, 'created profile')
		self.assertTrue(result)

	def test_follow_user_action(self):
		user_one = UserFactory.create(username='Stephen', password='Uytrewq123')
		user_two = UserFactory.create(username='Logan', password='Uytrewq123')
		Contact.objects.get_or_create(user_from=user_one, user_to=user_two)

		#utils.create_action returns True if one user followed another one
		result = utils.create_action(user_one, 'is following', user_two)
		self.assertTrue(result)

	def test_user_image_bookmark(self):
		user = UserFactory(username='Bob', password='Uytrewq123')
		image = ImageFactory(
			title='new_image', 
			url='https://itproger.com/news/hudshie-i-pri-etom-samie-populyarnie-paroli-top-10-za-10-let',
			description='',
			user=user
		)

		#utils.create_action returns True if user bookmarked an image
		result = utils.create_action(user, 'bookmarked image', image)
		self.assertTrue(result)

	def test_user_image_like(self):
		user = UserFactory(username='Sam', password='Uytrewq123')
		image = ImageFactory(
			title='new_image', 
			url='https://itproger.com/news/hudshie-i-pri-etom-samie-populyarnie-paroli-top-10-za-10-let',
			description='',
			user=user
		)
		image.users_like.add(user)

		#utils.create_action returns True if user liked an image
		result = utils.create_action(user, 'liked', image)	
		self.assertTrue(result)





