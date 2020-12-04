from django import forms

class USForm(forms.Form):
	channel_title = forms.CharField(required=True, label='Channel name:')
	video_id = forms.CharField(required=False, label='Video ID:')
	publish_date = forms.DateField(required=False, label='Publish Date:')
	category_id = forms.IntegerField(required=False, label='Category ID:')
	tags = forms.CharField(required=False, label='Tags:')

COUNTRIES = [
  ('GB', 'Great Britain'),
  ('CA', 'Canada'),
  ('DE', 'Germany'),
  ('US', 'United States')
]

class countriesForm(forms.Form):
	country = forms.CharField(required=True, label='Country')
	channel_title = forms.CharField(required=False, label='Channel name:')
	video_id = forms.CharField(required=False, label='Video ID:')
	publish_date = forms.DateField(required=False, label='Publish Date:')
	category_id = forms.IntegerField(required=False, label='Category ID:')
	tags = forms.CharField(required=False, label='Tags:')
	country= forms.CharField(label='Choose a country', widget=forms.Select(choices=COUNTRIES))


#MAKE FORMS FOR INSERT/DELETE/UPDATE
class InsertForm(forms.Form):
	country= forms.CharField(required=True, label='Choose a country', widget=forms.Select(choices=COUNTRIES))
	channel_title = forms.CharField(required=True, label='Channel name:')
	video_id = forms.CharField(required=True, label='Video ID:')
	title = forms.CharField(required=True, label='Video title:')
	trending_date = forms.DateField(required=True, label='Trending date:')
	publish_date = forms.DateField(required=True, label='Publish Date:')
	category_id = forms.IntegerField(required=True, label='Category ID:')
	views = forms.CharField(required=True, label='Views:')
	likes = forms.CharField(required=True, label='Likes:')
	dislikes = forms.CharField(required=True, label='Dislikes:')
	comment_count = forms.CharField(required=True, label='Comment count:')

	# Compares the published date and trending date of inserted video
	# Makes sure that a video doesn't trend before it publishes because that would make no fucking sense
	# User validation test case
	def clean_publish_date(self):
		cleaned_data = super(InsertForm, self).clean()
		trending_date = cleaned_data['trending_date']
		publish_date = cleaned_data['publish_date']
		if publish_date > trending_date :
			raise forms.ValidationError("Publish date should not be before the trending date.")
		return cleaned_data
	
class DeleteForm(forms.Form):
	country= forms.CharField(required=True, label='Choose a country', widget=forms.Select(choices=COUNTRIES))
	channel_title = forms.CharField(required=True, label='Channel name:')
	
class UpdateForm(forms.Form):
	country= forms.CharField(required=True, label='Choose a country', widget=forms.Select(choices=COUNTRIES))
	channel_title = forms.CharField(required=True, label='Channel name:')
	video_id = forms.CharField(required=False, label='Video ID:')
	trending_date = forms.CharField(required=False, label='Trending date:')
	publish_date = forms.CharField(required=False, label='Publish Date:')
	category_id = forms.IntegerField(required=False, label='Category ID:')
	views = forms.CharField(required=False, label='Views:')
	likes = forms.CharField(required=False, label='Likes:')
	dislikes = forms.CharField(required=False, label='Dislikes:')
	comment_count = forms.CharField(required=False, label='Comment count:')