from django.db import models
from django.contrib.auth.models import User

class categoryS(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    image = models.ImageField(upload_to='products/', default='default.png')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=400)
    Link = models.CharField(max_length=255)
    File = models.FileField()
    isActive = models.BooleanField(default=True)
    By = models.CharField(max_length=30)
    price = models.IntegerField()
    cat = models.ForeignKey(categoryS, on_delete=models.CASCADE, related_name='Product')

    def __str__(self):
        return f'{self.name} ({self.price}$)'
    
    def get_stripe_price(self):
        """Return price in cents for Stripe"""
        return self.price * 100

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    stripe_charge_id = models.CharField(max_length=100)
    amount = models.IntegerField()  # Store in cents
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment #{self.id} - Order #{self.order.id} - ${self.amount/100:.2f}"