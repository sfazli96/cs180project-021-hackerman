from django.shortcuts import render
from django.views import View
from .forms import USForm
from .helpers import *
from .analytics import *
from plotly.offline import plot
import plotly.graph_objs as go
from hackerman import urls

def home(request):
	return render(request, 'home.html', {})

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
			search = searchCSV(data)
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

def averagePerCategory(request):
	context = {}
	avg_per = avg_per_cat()

	categories = list(avg_per.keys())
	avg_likes = [avg_per[cat]['avg_likes'] for cat in categories]
	avg_dislikes = [avg_per[cat]['avg_dislikes'] for cat in categories]
	avg_views = [avg_per[cat]['avg_views'] for cat in categories]
	likes_fig = go.Figure(data=[go.Bar(x=categories, y=avg_likes)], layout=go.Layout(title='Average Likes Per Category in the USA', yaxis={'title': 'Likes'}, xaxis={'title': 'Categories'}))
	dislikes_fig = go.Figure(data=[go.Bar(x=categories, y=avg_dislikes)], layout=go.Layout(title='Average Dislikes Per Category in the USA', yaxis={'title': 'Dislikes'}, xaxis={'title': 'Categories'}))
	views_fig = go.Figure(data=[go.Bar(x=categories, y=avg_views)], layout=go.Layout(title='Average Views Per Category in the USA', yaxis={'title': 'Views'}, xaxis={'title': 'Categories'}))
	likes_div = plot(figure_or_data=likes_fig, output_type='div')
	dislikes_div = plot(figure_or_data=dislikes_fig, output_type='div')
	views_div = plot(figure_or_data=views_fig, output_type='div')
	context['likes_div'] = likes_div
	context['dislikes_div'] = dislikes_div
	context['views_div'] = views_div
	return render(request, 'avgPerCat.html', context)

# Analytics for the Top 20 Most Liked Videos
# Ranks the Top 20 Most Liked Videos in the CSV files
# Calculates the average number of likes per video (out of the Top 20)
def top20MostLiked(request):
	context = {}
	mostLiked = top_20_most_liked()

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
	mostDisliked = top_20_most_disliked()

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