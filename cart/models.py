from django.db import models
from store.models import Product, Variation



class Cart(models.Model):
  cart_id = models.CharField(max_length=200)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.cart_id


class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  #we are storing product_variation from add_cart views here using the Variation model:
  variations = models.ManyToManyField(Variation, blank=True) 
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  is_active = models.BooleanField(default=True)

  def sub_total(self):
    return self.product.price * self.quantity
#use unicode instead of str for product
  def __unicode__(self):
    return self.product
