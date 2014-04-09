from django.shortcuts import render, render_to_response

#from perf_app import models

def index(request):
    return render_to_response('index.html')



# Create your views here.
