from django.shortcuts import render, redirect
from .models import *
from store.models import Product
from django.http import HttpResponse





# we need when we click add to cart, get redirected to cart page and product to be added as well
# the process of adding to cart create a session key
# to store session key/id as cart_id with a private function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# adding product to a cart, we need its product_id


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        #getting the cart using the cart_id present in the session
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

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )

        cart_item.save()

    # return HttpResponse(cart_item.product)
    # exit()
    return redirect('cart')


def cart(request, total=0, quantity = 0, cart_items = None):
    try:
        #getting from session key
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active=True)
        for cart_item in cart_items:
            total+= cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
    except object.DoesNotExist:
        pass
        
    context = {
        'cart' : cart,
        'cart_items': cart_items,
        'total':total,
        'quantity': quantity
    }
    return render(request, 'cart/cart.html', context)


