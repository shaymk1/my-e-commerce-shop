from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from cart.models import CartItem
from category.models import Category
from .models import *
from cart.views import _cart_id
from django.db.models import Q

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


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
        # pagination
        paginator = Paginator(products, 3)
        page = request.GET.get('page')  # give us the requested page number
        paged_products = paginator.get_page(
            page)  # where we store the 6 products
        product_count = products.count()

    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        # pagination
        paginator = Paginator(products, 6)
        page = request.GET.get('page')  # give us the requested page number
        paged_products = paginator.get_page(
            page)  # where we store the 6 products
        product_count = products.count()

    context = {
        # 'products': products,
        # we no longer pass products, we now pass paged_products
        'products': paged_products,
        'product_count': product_count,
        'categories': categories,
        # 'paged_products ': paged_products
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    # products = Product.objects.filter(is_available=True)
    try:
     # category in store model and slug and category model we need access to
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
    # checking if product is already added to cart, starting with CartItem

        # __because cart is a foreugnkey of Cart and with cart we can access cart_id which is a field in Cart model
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart
        # 'products':products
    }

    return render(request, 'store/product-detail.html', context)


def search(request):
    # checking if the get request has the keyword, and store that value in keyword variable

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-date_created').filter(
                Q(description__icontains=keyword) |
                Q(product_name__icontains=keyword)
                # Q(category__icontains=keyword)

            )

            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)
