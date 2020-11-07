from django import forms

class USForm(forms.Form):
	channel_title = forms.CharField(required=True, label='Channel name:')
	video_id = forms.CharField(required=False, label='Video ID:')
	publish_date = forms.DateField(required=False, label='Publish Date:')
	category_id = forms.IntegerField(required=False, label='Category ID:')
	tags = forms.CharField(required=False, label='Tags:')



class countryForm(forms.Form):
	country = forms.CharField(required=True, label='Country')
	channel_title = forms.CharField(required=False, label='Channel name:')
	video_id = forms.CharField(required=False, label='Video ID:')
	publish_date = forms.DateField(required=False, label='Publish Date:')
	category_id = forms.IntegerField(required=False, label='Category ID:')
	tags = forms.CharField(required=False, label='Tags:')
	is_valid = forms.BooleanField(label='Is Valid', label_suffix=" : ",
                                  required=True, disabled=False,
                                  widget=forms.widgets.CheckboxInput(attrs={'class': 'checkbox-inline'}),
                                  help_text="Please check the box as this field is required.",
                                  error_messages={'required': "Please check the box"})

