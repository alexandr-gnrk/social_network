from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
from .views import Sub, Index, SubSession, web_hooks, Success, Cancel, Session, Portal

app_name = 'sub'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('subbbb/', Sub.as_view(), name='sub'),

    path('sub/session/', SubSession.as_view(), name='sub-session'),
    path('session/', Session.as_view(), name='session'),
    path('create-customer-portal-session/', Portal.as_view(), name='create-customer-portal-session'),


    path('success/', Success.as_view(), name='success'),
    path('cancel/', Cancel.as_view(), name='cancel'),
    path('webhooks/', web_hooks, name='webhooks'),
]


