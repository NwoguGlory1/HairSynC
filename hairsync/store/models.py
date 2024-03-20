"""HairSync Store Models."""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=False, default=slugify('default-category-slug'))

    def __str__(self):
        return self.name

    def to_dict(self, request=None):
        return {
            'category_id': self.category_id,
            'name': self.name,
            'slug': self.slug,
        }
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return f'{self.name} - {self.price}'

    def to_dict(self, request=None):
        image_url = self.image.url if self.image else None

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
