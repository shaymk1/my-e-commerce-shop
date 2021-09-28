from django.db import models
from django.urls import reverse
from category.models import Category

class Product(models.Model):
  product_name = models.CharField(max_length=50,blank=True, unique=True)
  slug = models.SlugField(unique=True)
  description = models.TextField(blank=True)
  image = models.ImageField(upload_to='photos/products')
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock =models.IntegerField()
  is_available = models.BooleanField(default=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  date_created = models.DateTimeField(auto_now=True)
  date_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.product_name
  
  


