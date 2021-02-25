from django.urls import path
from django.contrib.auth import views as auth_view
from . import views


urlpatterns = [
	#Обработчик действий со статьями
	path('login/', auth_view.LoginView.as_view(), name='login'),
	path('log-out/', auth_view.LogoutView.as_view(template_name='registration/log-out.html'), name='logout'),
	path('', views.dashboard, name='dashboard'),
	path('password_change/', auth_view.PasswordChangeView.as_view(), name='password_change'),
	path('password_change/done/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),
]