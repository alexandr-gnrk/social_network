from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'image', 'get_image', 'created']
	list_filter = ['created']

	def get_image(self, obj):
		if obj.image:
			return mark_safe(f'<img src="{obj.image.url}" width="75">')
