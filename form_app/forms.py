from django.forms import ModelForm
from .models import US

class USForm(ModelForm):
	class Meta:
		model = US
		fields = '__all__'