from django.shortcuts import render
from django.views import View
from .forms import *
from .helpers import *
from .analytics import *
from plotly.offline import plot
import plotly.graph_objs as go
from hackerman import urls
from google_drive_downloader import GoogleDriveDownloader as gdd
import pathlib
import time


def home(request):
	return render(request,'home.html',{})

def modifyDataset(request):
	template_name = 'modifyDataset.html'
	context = {}
	data = {}

	if request.method=='GET':
		insert_form = InsertForm()
		delete_form = DeleteForm()
		update_form = UpdateForm()
		context['insert_form'] = insert_form
		context['delete_form'] = delete_form
		context['update_form'] = update_form

	elif request.method=='POST':
		
		if request.POST.get('insert'):
			insert_form = InsertForm(request.POST)
			context['insert_form'] = insert_form
			if insert_form.is_valid():
				button_press = request.POST.get('insert')
				data['country'] = insert_form.cleaned_data.get('country')
				data['channel_title'] = insert_form.cleaned_data.get('channel_title')
				data['title'] = insert_form.cleaned_data.get('title')
				data['video_id'] = insert_form.cleaned_data.get('video_id')
				data['trending_date'] = insert_form.cleaned_data.get('trending_date')
				data['publish_date'] = insert_form.cleaned_data.get('publish_date')
				data['category_id'] = insert_form.cleaned_data.get('category_id')
				data['views'] = insert_form.cleaned_data.get('views')
				data['likes'] = insert_form.cleaned_data.get('likes')
				data['dislikes'] = insert_form.cleaned_data.get('dislikes')
				data['comment_count'] = insert_form.cleaned_data.get('comment_count')
				context['button_press'] = button_press
				insert(data)
		elif request.POST.get('delete'):
			delete_form = DeleteForm(request.POST)
			context['delete_form'] = delete_form
			if delete_form.is_valid():
				button_press = request.POST.get('delete')
				data['country'] = delete_form.cleaned_data.get('country')
				data['channel_title'] = delete_form.cleaned_data.get('channel_title')
				context['button_press'] = button_press
				delete(data)
		elif request.POST.get('update'):
			update_form = UpdateForm(request.POST)
			context['update_form'] = update_form
			if update_form.is_valid():
				button_press = request.POST.get('update')
				data['country'] = update_form.cleaned_data.get('country')
				data['channel_title'] = update_form.cleaned_data.get('channel_title')
				data['video_id'] = update_form.cleaned_data.get('video_id')
				data['trending_date'] = update_form.cleaned_data.get('trending_date')
				data['publish_date'] = update_form.cleaned_data.get('publish_date')
				data['category_id'] = update_form.cleaned_data.get('category_id')
				data['views'] = update_form.cleaned_data.get('views')
				data['likes'] = update_form.cleaned_data.get('likes')
				data['dislikes'] = update_form.cleaned_data.get('dislikes')
				data['comment_count'] = update_form.cleaned_data.get('comment_count')
				context['button_press'] = button_press
				update(data)

	return render(request, template_name, context)

class UnitedStatesView(View):
	template_name = 'US.html'
	form = USForm

	def get(self, request):
		data = {}
		context = {}
		form = USForm()
		#print(global_data)
		data['channel_title'] = request.GET.get('channel_title')
		data['video_id'] = request.GET.get('video_id')
		data['publish_time'] = request.GET.get('publish_time')
		data['category_id'] = request.GET.get('category_id')
		data['tags'] = request.GET.get('tags')
		if request.GET.get('channel_title'):
			search = searchCSV(data, 'US')
			context['search'] = search
			#print(search)
		context['form'] = form
		context['data'] = data
		return render(request, self.template_name, context)

	# EXAMPLE OF POST
	def post(self, request):
		data = {}
		form = USForm(request.POST)
		submitbutton = request.POST.get('Submit')
		if form.is_valid():
			data['video_id'] = form.cleaned_data.get('video_id')
			data['channel_title'] = form.cleaned_data.get('channel_title')
			data['publish_date'] = form.cleaned_data.get('publish_date')
			data['category_id'] = form.cleaned_data.get('category_id')
			data['tags'] = form.cleaned_data.get('tags')
			
			# Call helper functions depending on button pressed
			# Such as if submitbutton or if insert
		context = {'form': form, 'data': data, 'submitbutton': submitbutton}

		return render(request, self.template_name, context)

class CountriesView(View):
	template_name = 'countries.html'
	form = countriesForm

	def get(self, request):
		data = {}
		context = {}
		form = countriesForm()
		#print(global_data)
		data['country'] = request.GET.get('country')
		data['channel_title'] = request.GET.get('channel_title')
		data['video_id'] = request.GET.get('video_id')
		data['publish_time'] = request.GET.get('publish_time')
		data['category_id'] = request.GET.get('category_id')
		data['tags'] = request.GET.get('tags')
		if request.GET.get('channel_title'):
			search = searchCSV(data, data['country'])
			context['search'] = search
			context['size'] = len(search['channel_title'])
		#print(search)
		context['form'] = form
		context['data'] = data
		return render(request, self.template_name, context)

	# EXAMPLE OF POST
	def post(self, request):
		data = {}
		form = countriesForm(request.POST)
		submitbutton = request.POST.get('Submit')
		if form.is_valid():
			data['country'] = form.cleaned_data.get('country')
			data['video_id'] = form.cleaned_data.get('video_id')
			data['channel_title'] = form.cleaned_data.get('channel_title')
			data['publish_date'] = form.cleaned_data.get('publish_date')
			data['category_id'] = form.cleaned_data.get('category_id')
			data['tags'] = form.cleaned_data.get('tags')

		# Call helper functions depending on button pressed
		# Such as if submitbutton or if insert
		context = {'form': form, 'data': data, 'submitbutton': submitbutton}
		return render(request, self.template_name, context)

def averagePerCategory(request):
	time1 = time.perf_counter()
	context = {}
	#avg_per = avg_per_cat()

	categories = list(urls.averages.keys())
	avg_likes = [urls.averages[cat]['avg_likes']['numerator']/urls.averages[cat]['avg_likes']['denominator'] for cat in categories]
	avg_dislikes = [urls.averages[cat]['avg_dislikes']['numerator']/urls.averages[cat]['avg_dislikes']['denominator'] for cat in categories]
	avg_views = [urls.averages[cat]['avg_views']['numerator']/urls.averages[cat]['avg_views']['denominator'] for cat in categories]
	likes_fig = go.Figure(data=[go.Bar(x=categories, y=avg_likes)], layout=go.Layout(width=800, height=450, title='Average Likes Per Category in the USA', yaxis={'title': 'Likes'}, xaxis={'title': 'Categories'}))
	dislikes_fig = go.Figure(data=[go.Bar(x=categories, y=avg_dislikes)], layout=go.Layout(width=800, height=450, title='Average Dislikes Per Category in the USA', yaxis={'title': 'Dislikes'}, xaxis={'title': 'Categories'}))
	views_fig = go.Figure(data=[go.Bar(x=categories, y=avg_views)], layout=go.Layout(width=800, height=450, title='Average Views Per Category in the USA', yaxis={'title': 'Views'}, xaxis={'title': 'Categories'}))
	likes_div = plot(figure_or_data=likes_fig, output_type='div')
	dislikes_div = plot(figure_or_data=dislikes_fig, output_type='div')
	views_div = plot(figure_or_data=views_fig, output_type='div')
	context['likes_div'] = likes_div
	context['dislikes_div'] = dislikes_div
	context['views_div'] = views_div
	time2 = time.perf_counter()
	print('This view took:', time2-time1, 'seconds')
	return render(request, 'avgPerCat.html', context)


# Analytics for the Top 20 Most Liked Videos
# Ranks the Top 20 Most Liked Videos in the CSV files
# Calculates the average number of likes per video (out of the Top 20)
def top20MostLiked(request):
	context = {}
	mostLikedTemp2 = {}
	countries_list = ['US', 'GB', 'DE', 'CA']

	for country in countries_list:
		mostLikedTemp = top_20_most_liked(country)
		mostLikedTemp2.update(mostLikedTemp)

	# Sort the dictionary from most to least likes, and then push the top 20 results into another dictionary file
	k = Counter(mostLikedTemp2)
	mostLiked = dict(k.most_common(20))

	# Split the dictionary into two separate lists
	most_liked_keys = []
	most_liked_vals = []
	items = mostLiked.items()
	for item in items:
		most_liked_keys.append(item[0]), most_liked_vals.append(item[1])

	most_likes_fig = go.Figure(data=[go.Bar(x=most_liked_keys, y=most_liked_vals)], layout=go.Layout(title='<b>Top 20 Most Liked Videos', yaxis={'title': '<b>Likes'}, xaxis={'title': '<b>Video Name'}))
	mostLikedDiv = plot(figure_or_data=most_likes_fig, output_type='div')
	context['mostLikedDiv'] = mostLikedDiv

	# Create a box that outputs the average number of likes
	average_most_likes = 0

	for i in most_liked_vals:
		average_most_likes += i

	average_most_likes = average_most_likes / len(most_liked_vals)
	context['averageMostLikes'] = average_most_likes

	return render(request, 'top20MostLiked.html', context)

# Analytics for the Top 20 Most Disliked Videos
# Ranks the Top 20 Most Disliked Videos in the CSV files
# Calculates the average number of dislikes per video (out of the Top 20)
def top20MostDisliked(request):
	context = {}
	mostDislikedTemp2 = {}
	countries_list = ['US', 'GB', 'DE', 'CA']

	for country in countries_list:
		mostDislikedTemp = top_20_most_disliked(country)
		mostDislikedTemp2.update(mostDislikedTemp)

	# Sort the dictionary from most to least dislikes, and then push the top 20 results into another dictionary file
	k = Counter(mostDislikedTemp2)
	mostDisliked = dict(k.most_common(20))

	# Split the dictionary into two separate lists
	most_disliked_keys = []
	most_disliked_vals = []
	items = mostDisliked.items()
	for item in items:
		most_disliked_keys.append(item[0]), most_disliked_vals.append(item[1])

	most_dislikes_fig = go.Figure(data=[go.Bar(x=most_disliked_keys, y=most_disliked_vals)], layout=go.Layout(title='<b>Top 20 Most Disliked Videos', yaxis={'title': '<b>Dislikes'}, xaxis={'title': '<b>Video Name'}))
	mostDislikedDiv = plot(figure_or_data=most_dislikes_fig, output_type='div')
	context['mostDislikedDiv'] = mostDislikedDiv

	# Create a box that outputs the average number of dislikes
	average_most_dislikes = 0

	for i in most_disliked_vals:
		average_most_dislikes += i

	average_most_dislikes = average_most_dislikes / len(most_disliked_vals)
	context['averageMostDislikes'] = average_most_dislikes

	return render(request, 'top20MostDisliked.html', context)

# Analytics for countries that disable their comments section and likes/dislikes bar
# Calculate the number of disabled videos for each dataset, and then put those restuls into a pie chart
def disabledCommentsAndRatings(request):
	# FOR DISABLED COMMENTS
	context = {}
	comments_pass = 1
	ratings_pass = 2
	disabled_comments_vids = disabled(comments_pass)

	# Split dictionary into two lists
	disabled_comments_keys = []
	disabled_comments_vals = []
	comments_items = disabled_comments_vids.items()
	for item in comments_items:
		disabled_comments_keys.append(item[0]), disabled_comments_vals.append(item[1])

	disabled_comments_fig = go.Figure(data=[go.Pie(labels=disabled_comments_keys, values=disabled_comments_vals)])
	disabledCommentsFig = plot(figure_or_data=disabled_comments_fig, output_type='div')
	context['disabledCommentsFig'] = disabledCommentsFig

	# FOR DISABLED RATINGS
	disabled_ratings_vids = disabled(ratings_pass)

	disabled_ratings_keys = []
	disabled_ratings_vals = []
	ratings_items = disabled_ratings_vids.items()
	for item in ratings_items:
		disabled_ratings_keys.append(item[0]), disabled_ratings_vals.append(item[1])

	disabled_ratings_fig = go.Figure(data=[go.Pie(labels=disabled_ratings_keys, values=disabled_ratings_vals)])
	disabledRatingsFig = plot(figure_or_data=disabled_ratings_fig, output_type='div')
	context['disabledRatingsFig'] = disabledRatingsFig

	return render(request, 'disabledCommentsAndRatings.html', context)

def mostPopularCategory(request):
    context = {}

	# For the US
    most_popular_US = most_popular_categories('US')
	
	# For later, should sort the categories alphabetically
    #categories_US_temp = list(most_popular_US.keys())
    #categories_US = sorted(categories_US_temp)

    categories_US = list(most_popular_US.keys())
    video_views_US = [most_popular_US[cat]['video_views'] for cat in categories_US]
    views_fig_US = go.Figure(data=[go.Bar(x=categories_US, y=video_views_US)], layout=go.Layout(width=800, height=450, title='Most Popular Per Category in the USA', yaxis={'title': 'Views'}, xaxis={'title': 'Categories'}))
    viewsDivUS = plot(figure_or_data=views_fig_US, output_type='div')
    context['viewsDivUS'] = viewsDivUS

	# For Canada
    most_popular_CA = most_popular_categories('CA')

	# Problem: Canada has a None present in the dictionary, need to filter our categories_CA_temp to get rid of it first
    #categories_CA_temp = list(most_popular_CA.keys())
    #categories_CA = sorted(categories_CA_temp)
    
    categories_CA = list(most_popular_CA.keys())
    video_views_CA = [most_popular_CA[cat]['video_views'] for cat in categories_CA]
    views_fig_CA = go.Figure(data=[go.Bar(x=categories_CA, y=video_views_CA)], layout=go.Layout(width=800, height=450, title='Most Popular Per Category in Canada', yaxis={'title': 'Views'}, xaxis={'title': 'Categories'}))
    viewsDivCA = plot(figure_or_data=views_fig_CA, output_type='div')
    context['viewsDivCA'] = viewsDivCA

	# For Germany
    most_popular_DE = most_popular_categories('DE')
	
	# For later, should sort the categories alphabetically
    #categories_DE_temp = list(most_popular_DE.keys())
    #categories_DE = sorted(categories_DE_temp)

    categories_DE = list(most_popular_DE.keys())
    video_views_DE = [most_popular_DE[cat]['video_views'] for cat in categories_DE]
    views_fig_DE = go.Figure(data=[go.Bar(x=categories_DE, y=video_views_DE)], layout=go.Layout(width=800, height=450, title='Most Popular Per Category in Germany', yaxis={'title': 'Views'}, xaxis={'title': 'Categories'}))
    viewsDivDE = plot(figure_or_data=views_fig_DE, output_type='div')
    context['viewsDivDE'] = viewsDivDE

	# For Great Britain
    most_popular_GB = most_popular_categories('GB')
	
	# For later, should sort the categories alphabetically
    #categories_GB_temp = list(most_popular_GB.keys())
    #categories_GB = sorted(categories_GB_temp)

    categories_GB = list(most_popular_GB.keys())
    video_views_GB = [most_popular_GB[cat]['video_views'] for cat in categories_GB]
    views_fig_GB = go.Figure(data=[go.Bar(x=categories_GB, y=video_views_GB)], layout=go.Layout(width=800, height=450, title='Most Popular Per Category in Great Britain', yaxis={'title': 'Views'}, xaxis={'title': 'Categories'}))
    viewsDivGB = plot(figure_or_data=views_fig_GB, output_type='div')
    context['viewsDivGB'] = viewsDivGB
	
    return render(request, 'mostPopularCategory.html', context) 

def about(request):
	return render(request, 'about.html', {})

# Returns the Top 25 videos with the most active comments sections for each country
def mostActiveComments(request):
	context = {}
	mostCommentedTemp2 = {}
	countries_list = ['US', 'GB', 'DE', 'CA']

	for country in countries_list:
		mostCommentedTemp = most_active_comments(country)
		mostCommentedTemp2.update(mostCommentedTemp)

	# Sort the dictionary from most to least comment_count, and then push the top 20 results into another dictionary file
	k = Counter(mostCommentedTemp2)
	mostCommented = dict(k.most_common(25))

	# Split the dictionary into two separate lists
	most_commented_keys = []
	most_commented_vals = []
	items = mostCommented.items()
	for item in items:
		most_commented_keys.append(item[0]), most_commented_vals.append(item[1])

	most_commented_fig = go.Figure(data=[go.Bar(x=most_commented_keys, y=most_commented_vals)], layout=go.Layout(title='<b>Top 25 Most Active Comments Sections', yaxis={'title': '<b>Number of Comments'}, xaxis={'title': '<b>Video Name'}))
	mostCommentedDiv = plot(figure_or_data=most_commented_fig, output_type='div')
	context['mostCommentedDiv'] = mostCommentedDiv

	# Create a box that outputs the average number of likes
	average_most_comments = 0

	for i in most_commented_vals:
		average_most_comments += i

	average_most_comments = average_most_comments / len(most_commented_vals)
	context['averageMostComments'] = average_most_comments

	return render(request, 'mostCommented.html', context)
