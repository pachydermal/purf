#!/usr/local/python/current/bin/python
import _ssl;_ssl.PROTOCOL_SSLv23 = _ssl.PROTOCOL_SSLv3

from django.shortcuts import render
import CASClient, os

def index(request):
    return render(request, 'index.html')
