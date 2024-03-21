"""HairSync Store Models."""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
  #  slug = models.SlugField(max_length=255, unique=True, editable=False)

    def __str__(self):
        return self.name

    def to_dict(self, request=None):
        return {
            'category_id': self.category_id,
            'name': self.name,
          #  'slug': self.slug,
        }
    
    # def save(self, *args, **kwargs):
    #    if not self.slug:
    #        self.slug = slugify(self.name)
    #    super(Category, self).save(*args, **kwargs)


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


class ShoppingCart(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f'Cart ID: {self.cart_id} - User: {self.user}'

    def to_dict(self, request=None):
        cart_dict = {
            'cart_id': self.cart_id,
            'user': self.user.username,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'status': self.status,
        }

        cart_items = self.cartitem_set.all()
        cart_dict['items'] = [item.to_dict() for item in cart_items]

        return cart_dict


class CartItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Item ID: {self.item_id} - Product: {self.product.name} - Quantity: {self.quantity}'

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'cart': self.cart.to_dict() if self.cart else None,
            'product': self.product.to_dict() if self.product else None,
            'subtotal': self.product.price * self.quantity,
            'quantity': self.quantity,
        }


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order ID: {self.order_id} - User: {self.user.username} - Status: {self.order_status}'

    def to_dict(self, request=None):
        return {
            'order_id': self.order_id,
            'user': self.user.id,
            'total_amount': str(self.total_amount),
            'order_status': self.order_status,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class OrderItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item ID: {self.item_id} - Product: {self.product.name} - Quantity: {self.quantity}'

    def to_dict(self):
        return {
            'order_item_id': self.item_id,
            'order': self.order.order_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'unit_price': str(self.unit_price),
        }
