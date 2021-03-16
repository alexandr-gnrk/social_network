from django.contrib.auth.models import User

from images.models import Image
from django.urls import reverse
from images.tests.factory import UserFactory, ImageFactory
from django.test import TestCase


class ImagesTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.image = ImageFactory(user=self.user)
        # self.user = User.objects.create_user('user', password='test')
        # self.image = Image.objects.create(user=self.user, id=1, title='django', slug='django')
        self.client.login(username='user', password='test')

    # VIEWS
    def test_image_list_view(self):
        # self.client.login(username='John', password='test')
        response = self.client.get(reverse('images:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image/list.html')
        self.assertIn(self.image.title.encode('utf-8'), response.content)

    def test_image_create_view(self):
        response = self.client.get(reverse('images:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image/create.html')

    def test_image_create_view_post_fail_blank(self):
        response = self.client.post(reverse('images:create'), {})  # blank data dictionary
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_image_create_view_post_fail_invalid(self):
        response = self.client.post(reverse('images:create'), {'url': 'something', 'description': 'something'})
        # Where "form" is the context variable name for your form, "something" is the field name,
        # and "This field is required." is the exact text of the expected validation error.
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_image_detail_view(self):
        response = self.client.get(reverse('images:detail', kwargs={'id': self.image.id, 'slug': self.image.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image/detail.html')

    def test_image_ranking_view(self):
        response = self.client.get(reverse('images:ranking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image/ranking.html')

    # def test_image_like_view(self):
    #     data = {'action': 'like', '_selected_action': self.image.users_like.add(self.user)}
    #     print(data)
    #     response = self.client.post(reverse('images:like'), data, follow=True)
    #     self.assertEqual(Image.objects.filter(users_like__user=self.user).count(), 0)
    #     # self.assertEqual(response.status_code, 200)
    #     print(
    #         self.image.users_like.count(),
    #         Image.objects.filter(users_like__user=self.user).count()
    #     )

    # MODELS
    def test_image_model_creation(self):
        img = self.image
        self.assertTrue(isinstance(img, Image))
        self.assertEqual(img.__str__(), img.title)

    def test_image_models_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEqual(self.image.get_absolute_url(), '/images/detail/1/django/')
