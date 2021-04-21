from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import SimpleRouter

from . import views
from .views import ChangePasswordView, SendMailView, UserViewSet, DashboardView, UserFollowView


router = SimpleRouter()
router.register(r'api', UserViewSet, basename='api')


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/log-out.html'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('', include('django.contrib.auth.urls')),

    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),

    # api
    path('api/auth/', views.AuthAPIView.as_view(), name='api_auth'),
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),

    path('api/change-password/', ChangePasswordView.as_view()),
    path('api/send/', SendMailView.as_view()),
    path('api/dashboard/', DashboardView.as_view()),
    path('api/users/follow/', UserFollowView.as_view()),
]
urlpatterns += router.urls
