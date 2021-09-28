from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from category.models import Category
from .models import *

def home(request):
  context={}
  return render(request, 'store/home.html', context)
def store(request, category_slug = None):
  categories = None
  products = None

  if category_slug !=None:
    categories = get_object_or_404(Category, slug = category_slug)
    products = Product.objects.filter(category=categories, is_available=True)
    product_count =products.count()

  else:
    products = Product.objects.filter(is_available=True)
    product_count = products.count()

  
  
  context = {
    'products':products,
    'product_count':product_count
  }
  return render(request, 'store/store.html', context)


