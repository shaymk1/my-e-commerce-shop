from django.db import models
from django.urls import reverse


class Category(models.Model):
  category_name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(unique=True)

  class Meta:
    verbose_name = 'category'
    verbose_name_plural = 'categories'

  def __str__(self):
    return self.category_name
