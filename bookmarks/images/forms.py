from djamgo import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'url', 'description')
		widgets = {'url': forms.HiddenInput,}

	def clean_url(self):
		url = self.cleaned_data['url']
		valid_extensions = ['jpg', 'jpeg']
		extension = url.split('.', 1)[1].lower()
		if not extension in valid_extensions:
			raise forms.ValidationError('The given URL does not match valid image extensions.')
		return url