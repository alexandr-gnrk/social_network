from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'get_photo']

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')

    get_photo.short_description = 'Photo'


UserAdmin.list_display += ('is_superuser', 'stripe_id')
# UserAdmin.list_filter += ('paid_until',)
