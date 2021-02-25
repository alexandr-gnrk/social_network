from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
	# Обработчик действий со статьями
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='registration/log-out.html'), name='logout'),
	path('', views.dashboard, name='dashboard'),
	path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
	path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
	path('edit/', views.edit, name='edit'),

    # Обработчики восстановления пароля.
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include('django.contrib.auth.urls')), # Делает то же самое что и закомментированные сверху строки

    path('register/', views.register, name='register'),
]

