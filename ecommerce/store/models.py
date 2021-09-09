from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user    = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name    = models.CharField(max_length=200, null=True)
    email   = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image   = models.ImageField(upload_to='products_imgs', null=True, blank=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    def get_items(self):
        return self.items.all()
    
    def update_item(self, product, action):
        order_item, _ = self.items.get_or_create(product=product)
        
        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            order_item.quantity -= 1
        
        if order_item.quantity <= 0:
            order_item.delete()
        else:
            order_item.save()
        return order_item
    
    @classmethod
    def get_opened_order(cls, customer):
        order, _ = cls.objects.get_or_create(customer=customer, complete=False)
        return order

    @property
    def number_of_items(self):
        return sum(self.items.values_list('quantity', flat=True))

    @property
    def total(self):
        sum = 0
        for item in self.items.all():
            sum += item.total 
        return float(f'{sum:.2f}')

    @property
    def shipping(self):
        return self.items.filter(product__digital=False).exists()


class OrderItem(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order       = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity    = models.PositiveSmallIntegerField(default=0)
    date_added  = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return self.product.name

    @property
    def price(self):
        return float(f'{self.product.price:.2f}')

    @property
    def image(self):
        return self.product.image
    
    @property
    def total(self):
        return float(f'{self.quantity * self.product.price:.2f}')

class ShippingAddress(models.Model):
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order       = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address     = models.CharField(max_length=500)
    city        = models.CharField(max_length=100)
    zipcode     = models.CharField(max_length=100)
    date_added  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
