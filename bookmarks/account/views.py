import os

from decouple import config
from django.core.mail import send_mass_mail
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
import json

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.decorators import ajax_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact

from django.contrib import messages
from actions.utils import create_action
from actions.models import Action

#API
from rest_framework import generics, permissions, status
from .api.serializers import RegisterSerializer, ChangePasswordSerializer, ContactsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .tasks import send_mail_task

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


@login_required
def dashboard(request):
    # Display of all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # If the current user has subscribed to somebody, 
        # only actions of these users will be displayed.
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people', 'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})


#API
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny,]
    serializer_class = RegisterSerializer


class AuthAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(Q(username__iexact=data['username']) | Q(email__iexact=data['username']))
        if user.exists():
            user = user.first()
            if user.check_password(data['password']):
                if user.is_active:
                    payload     = jwt_payload_handler(user)
                    token       = jwt_encode_handler(payload)
                    response    = jwt_response_payload_handler(token, user, request)
                    return Response(response)
                return Response({'detail': 'Your account has been disabled'}, status=400)
            return Response({'detail': 'Invalid username or password'}, status=400)
        return Response({'detail': 'User does not exist'}, status=400)


class ChangePasswordView(generics.UpdateAPIView):
    """ An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    # authentication_classes = {SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication}
    # permission_classes = (permissions.AllowAny,)

    # @method_decorator(ensure_csrf_cookie)
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    # @method_decorator(ensure_csrf_cookie)
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactsView(APIView):
    """ View for sending mail to all users
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email_list = list(User.objects.all().values_list('email', flat=True))

        serializer = ContactsSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data["subject"]
            text = serializer.validated_data["text"]
            sender = config('EMAIL_HOST_USER')
            message = (subject, text, sender, email_list)
            send_mail_task.delay((message,), fail_silently=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
