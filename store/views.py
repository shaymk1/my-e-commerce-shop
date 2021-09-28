from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *


def home(request):
  context = {}
  return render(request, 'store/home.html', context)


