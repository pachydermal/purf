from django.shortcuts import render, render_to_response

#from perf_app import models

def index(request):
    return render_to_response('index.html')

def profile(request):
    return render_to_response('profile.html')


# Create your views here.
