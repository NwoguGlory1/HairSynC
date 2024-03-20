"""HairSync Store Models."""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def to_dict(self, request=None):
        return {
            'category_id': self.category_id,
            'name': self.name,
        }

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    price = models.PositiveIntegerField(null=False)
    quantity_in_stock = models.PositiveIntegerField(null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='images', null=False, blank=True)

    def __str__(self):
        return f'{self.name} - {self.price}'

    def to_dict(self, request=None):
        image_url = self.image.url

        if request and image_url:
            image_url = request.build_absolute_uri(image_url)

        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': str(self.price),
            'quantity_in_stock': self.quantity_in_stock,
            'category': self.category.to_dict() if self.category else None,
            'image': image_url
        }
