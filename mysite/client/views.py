from django.shortcuts import render
from django.views import View
from .forms import USForm, countryForm
from .helpers import *

def home(request):
	return render(request, 'home.html', {})

class UnitedStatesView(View):
	filepath = '/home/kratos/Documents/cs180project-021-hackerman/mysite/client/data/USvideos.csv'
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

class CountryView(View):
	filepath = '/home/kratos/Documents/cs180project-021-hackerman/mysite/client/data/GBvideos.csv'
	template_name = 'great_britain.html'
	form = countryForm

	def get(self, request):
		data = {}
		context = {}
		form = countryForm()
		data['country'] = request.GET.get('country')
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
		form = countryForm(request.POST)
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

class canadaView(View):
	filepath = '/home/kratos/Documents/cs180project-021-hackerman/mysite/client/data/CAvideos.csv'
	template_name = 'canada.html'
	form = countryForm

	def get(self, request):
		data = {}
		context = {}
		form = countryForm()
		data['country'] = request.GET.get('country')
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
		form = countryForm(request.POST)
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

def country(request):
	checkboxes_selected = request.POST.getlist('options[]')
	return render(request, 'country.html', {})

def action_page(request):
	return render(request, 'action_page.html', {})

