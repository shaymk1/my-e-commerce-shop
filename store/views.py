from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from category.models import Category
from .models import *


def home(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'store/home.html', context)

# to display products by category


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        product_count = products.count()

    else:
        products = Product.objects.filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'categories': categories
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    # products = Product.objects.filter(is_available=True)
    try:

        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)  # category in store model and slug and category model we need access to

    except Exception as e:
        raise e

    context = {
        'single_product': single_product
        # 'products':products
    }

    return render(request, 'store/product-detail.html', context)
