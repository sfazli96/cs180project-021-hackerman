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

CATEGORIES = [
	('1', 'Film & Animation'),
	('2', 'Autos & Vehicles'),
	('10', 'Music'),
	('15', 'Pets & Animals'),
	('17', 'Sports'),
	('18', 'Short Movies'),
	('19', 'Travel & Events'),
	('20', 'Gaming'),
	('21', 'Videoblogging'),
	('22', 'People & Blogs'),
	('23', 'Comedy'),
	('24', 'Entertainment'),
	('25', 'News & Politics'),
	('26', 'Howto & Style'),
	('27', 'Education'),
	('28', 'Science & Technology'),
	('29', 'Nonprofits & Activism'),
	('30', 'Movies'),
	('31', 'Anime/Animation'),
	('32', 'Action/Adventure'),
	('33', 'Classics'),
	('34', 'Comedy'),
	('35', 'Documentary'),
	('36', 'Drama'),
	('37', 'Family'),
	('38', 'Foreign'),
	('39', 'Horror'),
	('40', 'Sci-Fi/Fantasy'),
	('41', 'Thriller'),
	('42', 'Shorts'),
	('43', 'Shows'),
	('44', 'Trailers')
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
	trending_date = forms.CharField(required=True, label='Trending date (YY.DD.MM):')
	publish_date = forms.CharField(required=True, label='Publish Date (YYYY-MM-DDT, must include T at the end):')
	category_id = forms.CharField(required=True, label='Category ID:', widget=forms.Select(choices=CATEGORIES))
	views = forms.CharField(required=True, label='Views:')
	likes = forms.CharField(required=True, label='Likes:')
	dislikes = forms.CharField(required=True, label='Dislikes:')
	comment_count = forms.CharField(required=True, label='Comment count:')

	# Compares the published date and trending date of inserted video
	# Makes sure that a video doesn't trend before it publishes because that would make no fucking sense
	# User validation test case
	#def clean_publish_date(self):
	#	cleaned_data = super(InsertForm, self).clean()
	#	trending_date = cleaned_data['trending_date']
	#	publish_date = cleaned_data['publish_date']
	#	if publish_date > trending_date :
	#		raise forms.ValidationError("Publish date should not be before the trending date.")
	#	return cleaned_data
	
class DeleteForm(forms.Form):
	country= forms.CharField(required=True, label='Choose a country', widget=forms.Select(choices=COUNTRIES))
	channel_title = forms.CharField(required=True, label='Channel name:')
	
class UpdateForm(forms.Form):
	country= forms.CharField(required=True, label='Choose a country', widget=forms.Select(choices=COUNTRIES))
	channel_title = forms.CharField(required=True, label='Channel name:')
	video_id = forms.CharField(required=False, label='Video ID:')
	trending_date = forms.CharField(required=False, label='Trending date (YY.DD.MM):')
	publish_date = forms.CharField(required=False, label='Publish Date (YYYY-MM-DDT, must include T at the end):')
	category_id = forms.CharField(required=False, label='Category ID:', widget=forms.Select(choices=CATEGORIES))
	views = forms.CharField(required=False, label='Views:')
	likes = forms.CharField(required=False, label='Likes:')
	dislikes = forms.CharField(required=False, label='Dislikes:')
	comment_count = forms.CharField(required=False, label='Comment count:')