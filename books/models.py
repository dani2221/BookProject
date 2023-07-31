from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='books/')
    author = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.title} - {self.author}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.book} - {self.quantity}'


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    delivery_status = models.CharField(max_length=255, choices=[('new', 'New'), ('delivering', 'Delivering'), ('delivered', 'Delivered')])

    def __str__(self):
        return f'{self.full_name} - {self.delivery_status}'
