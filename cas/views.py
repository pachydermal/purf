#!/usr/local/python/current/bin/python
from django.shortcuts import render
import CASClient, os

def index(request):
    return render(request, 'index.html')
