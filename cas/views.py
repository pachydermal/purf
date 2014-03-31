#!/usr/local/python/current/bin/python
from django.shortcuts import render
import CASClient, os

def index(request):
    C = CASClient.CASClient()
    netid = C.Authenticate()
    print "Content-Type; text/html"
    print ""

    return render(request, 'index.html')
