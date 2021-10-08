from django.contrib import admin
from .models import *


class CartItemAdmin(admin.ModelAdmin):
  list_display = ('product', 'cart', 'quantity', 'is_active')
  list_filter = ('product', 'quantity', 'is_active')


admin.site.register( CartItem,CartItemAdmin)
admin.site.register(Cart)


