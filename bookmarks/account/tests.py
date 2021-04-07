from django.test import TestCase, Client
from django.urls import reverse
from account.models import Profile, Contact
from django.contrib.auth.models import User
from http_status_code.standard import successful_request
from http_status_code import StatusCode

from parameterized import parameterized
import requests

successful_post_request = StatusCode(201, 'You have been registered')


class AccountTestCase(TestCase):

    def setUp(self):
        self.test_username = 'test_user'
        self.test_email = 'test_email@email.com'
        self.test_password = 'VeRyStRoNg_password'
        user = User.objects.create_user(
            self.test_username,
            self.test_email,
            self.test_password)
        Profile.objects.create(user=user)
        
        self.client = Client()
        self.client.login(
            username=self.test_username,
            password=self.test_password)

    @parameterized.expand([
        ('dashboard',),
        ('edit',),
        ('user_list',),
        ('user_detail', ['test_user']),
    ])
    def test_page_redirecting_unathorized_users(self, page_name, args=None):
        self.client.logout()
        response = self.client.get(
            reverse(page_name, args = args))
        self.assertEquals(response.status_code, 302)

    @parameterized.expand([
        ('dashboard',),
        ('register',),
        ('edit',),
        ('user_list',),
        ('user_detail', ['test_user']),
    ])
    def test_page_is_reacheable(self, page_name, args=None):
        response = self.client.get(
            reverse(page_name, args=args))
        self.assertEquals(response.status_code, 200)

    @parameterized.expand([
        ('dashboard', 'account/dashboard.html'),
        ('register', 'account/register.html'),
        ('edit', 'account/edit.html'),
        ('user_list', 'account/user/list.html'),
        ('user_detail', 'account/user/detail.html', ['test_user']),
    ])
    def test_page_using_correct_template(self, page_name, template_path, args=None):
        response = self.client.get(
            reverse(page_name, args=args))
        self.assertTemplateUsed(response, template_path)

    def test_edit_page_is_updating_user_info(self):
        args = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'email': 'ivan79@mail.com',
        }
        response = self.client.post(
            reverse('edit'), args)

        user = User.objects.get(username=self.test_username)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(user.first_name, args['first_name'])
        self.assertEquals(user.last_name, args['last_name'])
        self.assertEquals(user.email, args['email'])

    # API tests

    def test_register_api(self):
        ENDPOINT = 'http://localhost:8000/api/register/'
        data = {
            'username'  : 'api_user16',
            'email'     : 'api_user16@api.com',
            'password'  : 'Uytrewq1234',
            'password2' : 'Uytrewq1234'
        }
        res = requests.post(ENDPOINT, data=data)
        self.assertEquals(res.status_code, successful_post_request.code)
        self.assertEquals('{"username":"api_user16","email":"api_user16@api.com"}', res.text)

    def test_auth_api(self):
        ENDPOINT = 'http://localhost:8000/api/auth/'
        data = {
            'username'  : 'api_user13',
            'password'  : 'Uytrewq1234'
        }
        res = requests.post(ENDPOINT, data=data)
        self.assertEquals(res.status_code, successful_request.code)