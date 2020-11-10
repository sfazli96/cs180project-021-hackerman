from django.shortcuts import render
from django.views import View
from .forms import USForm, countriesForm
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
            search = searchCountries(data)
            context['search'] = search
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

def top20MostLiked(request):
	context = {}
	mostLiked = top_20_most_liked()

	# Split the dictionary into two separate lists
	most_liked_keys = []
	most_liked_vals = []
	items = mostLiked.items()
	for item in items:
		most_liked_keys.append(item[0]), most_liked_vals.append(item[1])

	# Loops that print output of each list, only for testing
	'''for i in range(len(most_liked_keys)):
		print(most_liked_keys[i])

	for i in range(len(most_liked_vals)):
		print(most_liked_vals[i])'''

	most_likes_fig = go.Figure(data=[go.Bar(x=most_liked_keys, y=most_liked_vals)], layout=go.Layout(title='Top 20 Most Liked Videos', yaxis={'title': 'Likes'}, xaxis={'title': 'Video Name'[:12]}))
	mostLikedDiv = plot(figure_or_data=most_likes_fig, output_type='div')
	context['mostLikedDiv'] = mostLikedDiv
	return render(request, 'top20MostLiked.html', context)

def top20MostDisliked(request):
	context = {}
	mostDisliked = top_20_most_disliked()

	# Split the dictionary into two separate lists
	most_disliked_keys = []
	most_disliked_vals = []
	items = mostDisliked.items()
	for item in items:
		most_disliked_keys.append(item[0]), most_disliked_vals.append(item[1])

	# Loops that print output of each list, only for testing
	'''for i in range(len(most_disliked_keys)):
		print(most_disliked_keys[i])

	for i in range(len(most_disliked_vals)):
		print(most_disliked_vals[i])'''

	most_dislikes_fig = go.Figure(data=[go.Bar(x=most_disliked_keys, y=most_disliked_vals)], layout=go.Layout(title='Top 20 Most Disliked Videos', yaxis={'title': 'Dislikes'}, xaxis={'title': 'Video Name'[:12]}))
	mostDislikedDiv = plot(figure_or_data=most_dislikes_fig, output_type='div')
	context['mostDislikedDiv'] = mostDislikedDiv
	return render(request, 'top20MostDisliked.html', context)
