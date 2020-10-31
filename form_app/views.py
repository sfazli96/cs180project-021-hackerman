from django.shortcuts import render
from .forms import USForm


def index(request):

	form = USForm()

	if request.method == 'POST':
		form = USForm(request.POST)
		if form.is_valid():
			form.save()
			
	context = {'form':form}
	return render(request, 'app/index.html', context)