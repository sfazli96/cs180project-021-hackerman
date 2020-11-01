from django import forms

class USForm(forms.Form):
	video_id = forms.CharField(required=True, label='Video ID:')
	channel_title = forms.CharField(required=False, label='Channel name:')
	publish_date = forms.DateField(required=False, label='Publish Date:')
	category_id = forms.IntegerField(required=False, label='Category ID:')
	tags = forms.CharField(required=False, label='Tags:')
