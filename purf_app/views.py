from django.shortcuts import render, render_to_response
from purf_app.models import Professor
#from perf_app import models

def index(request):
    return render_to_response('index.html')

def profile(request, id):
    prof = Professor.objects.get(pk=id)
    context ={'prof': prof}
    return render(request, 'profile.html', context)


# Create your views here.
