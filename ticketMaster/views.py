# Create your views here.
from django.shortcuts import render
from django.shortcuts import HttpResponse


def ticketmaster(request):
    return HttpResponse("Hello Ticket Master")
