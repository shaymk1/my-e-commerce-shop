from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from store.models import Product
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


# we need when we click add to cart, get redirected to cart page and product to be added as well
# the process of adding to cart create a session key
# to store session key/id as cart_id with a private function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# adding product to a cart, we need its product_id


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        # getting the cart using the cart_id present in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # getting the cart_item which = product + cart

    try:
        cart_item = CartItem.objects.get(
            product=product,
            cart=cart
        )

        cart_item.quantity += 1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart

        )

        cart_item.save()

    # return HttpResponse(cart_item.product)
    # exit()
    return redirect('cart')


def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        vat = 0
        grand_total = 0
        # getting from session key
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        vat = (15 * total)/100
        grand_total = total + vat
    except ObjectDoesNotExist:
        pass

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'grand_total': grand_total,
        'vat': vat
    }
    return render(request, 'cart/cart.html', context)
