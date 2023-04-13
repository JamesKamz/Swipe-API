from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_farmer=models.BooleanField(default=False)
    is_transporter=models.BooleanField(default=False)
    is_buyer=models.BooleanField( default=False)
    contact=models.CharField(max_length=20)

class Farmer(models.Model):
    user=models.OneToOneField(CustomUser, related_name='farmer', on_delete=models.CASCADE, primary_key=True)
    def  __str__(self):
        return f' Utilisateur: {self.user.username} | Nom: {self.user.last_name} | Prénoms: {self.user.first_name}'
        
class Buyer (models.Model):
    user=models.OneToOneField(CustomUser, related_name='buyer', on_delete=models.CASCADE, primary_key=True)
    def  __str__(self):
        return f' Utilisateur: {self.user.username} | Nom: {self.user.last_name} | Prénoms: {self.user.first_name}'
        
class Farm (models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    gps_latitude=models.DecimalField(max_digits=6, decimal_places=2)
    gps_longitude=models.DecimalField(max_digits=6, decimal_places=2)
    owner=models.ForeignKey(Farmer, on_delete=models.CASCADE)
    active=models.BooleanField(default=True)

    def  __str__(self):
        return f'{self.name} de {self.owner} situé à {self.address}'
    
    def create_farm(self):
        self.save

class Product(models.Model):
    place=models.ManyToManyField(Farm, related_name='location')
    name=models.CharField(max_length=100)
    description=models.TextField()
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=6, decimal_places=2)
    active=models.BooleanField(default=True)
    def __str__(self) -> str:
        return f'{self.name} de {self.quantity} sacs'
    
    def create_product(self):
        self.save

class Order (models.Model):
    order_date=models.DateTimeField(auto_now_add=True)
    delivery_date=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(Buyer, related_name='BuyerOrdering', on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    total_amount=models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.order_date
    
    def create_order(self):
        self.save()

class Transporter(models.Model):
    user=models.OneToOneField(CustomUser, related_name='transporter', on_delete=models.CASCADE, primary_key=True)
    def  __str__(self):
        return f' Utilisateur: {self.user.username} | Nom: {self.user.last_name} | Prénoms: {self.user.first_name}'
        
class  Transportation(models.Model):
    PLACES=(
        ('IN', 'In Farm'),
        ('IW', 'In Way'),
        ('AH', 'At Home'),
    )
    products=models.ManyToManyField(Order, related_name='transportorder')
    transporter=models.ForeignKey(Transporter, related_name='transportation', on_delete=models.CASCADE)
    current_place=models.CharField( max_length=5, choices=PLACES)
