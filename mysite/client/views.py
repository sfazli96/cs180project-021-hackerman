from django.shortcuts import render
from django.views import View
from .forms import USForm
from .helpers import *
from .analytics import *
from plotly.offline import plot
import plotly.graph_objs as go

def home(request):
	return render(request, 'home.html', {})

class UnitedStatesView(View):
	filepath = '/home/chair/Documents/UCRFall2020/CS180/project/cs180project-021-hackerman/mysite/client/data/USvideos.csv'
	template_name = 'US.html'
	form = USForm

	def get(self, request):
		data = {}
		context = {}
		form = USForm()
		data['channel_title'] = request.GET.get('channel_title')
		data['video_id'] = request.GET.get('video_id')
		data['publish_time'] = request.GET.get('publish_time')
		data['category_id'] = request.GET.get('category_id')
		data['tags'] = request.GET.get('tags')
		if request.GET.get('channel_title'):
			search = searchCSV(self.filepath, data)
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
	avg_per = avg_per_cat('/home/chair/Documents/UCRFall2020/CS180/project/cs180project-021-hackerman/mysite/client/data/USvideos.csv')

	categories = list(avg_per.keys())
	avg_likes = [avg_per[cat]['avg_likes'] for cat in categories]
	avg_dislikes = [avg_per[cat]['avg_dislikes'] for cat in categories]
	avg_views = [avg_per[cat]['avg_views'] for cat in categories]
	likes_div = plot([go.Bar(x=categories, y=avg_likes, name='Average Likes Per Category in the USA')], output_type='div')
	dislikes_div = plot([go.Bar(x=categories, y=avg_dislikes, name='Average Dislikes Per Category in the USA')], output_type='div')
	views_div = plot([go.Bar(x=categories, y=avg_views, name='Average Views Per Category in the USA')], output_type='div')
	context['likes_div'] = likes_div
	context['dislikes_div'] = dislikes_div
	context['views_div'] = views_div
	return render(request, 'avgPerCat.html', context)
