from django.db import models

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