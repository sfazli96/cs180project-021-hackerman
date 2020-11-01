from django.shortcuts import render
from django.views import View
from .forms import USForm
from .helpers import parseCSV

def home(request):
	return render(request, 'home.html', {})

class UnitedStatesView(View):
	template_name = 'US.html'
	form = USForm
	data_for_get = {}

	def get(self, request):
		context = {}
		print(self.data_for_get)
		context['data'] = self.data_for_get
		context['form'] = self.form
		return render(request, self.template_name, context)

	# EXMAPLE OF POST
	def post(self, request):
		form = USForm(request.POST)
		submitbutton = request.POST.get('Submit')
		if form.is_valid():
			self.data_for_get['video_id'] = form.cleaned_data.get('video_id')
			self.data_for_get['channel_title'] = form.cleaned_data.get('channel_title')
			self.data_for_get['publish_date'] = form.cleaned_data.get('publish_date')
			self.data_for_get['category_id'] = form.cleaned_data.get('category_id')
			self.data_for_get['tags'] = form.cleaned_data.get('tags')
		#print(self.data_for_get['video_id'])
		context = {'form': form, 'data': self.data_for_get, 'submitbutton': submitbutton}

		return render(request, self.template_name, context)
