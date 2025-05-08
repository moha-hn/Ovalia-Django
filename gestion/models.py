from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
# Create your models here.



class User(AbstractUser):
    email = models.EmailField(unique=False)  # champ supplémentaire, mais 'username' reste l'identifiant
    file = models.FileField(upload_to='diplomes/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username



class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/', blank=True)
    description = models.TextField(blank=True)
    cou = models.DecimalField(max_digits=10,decimal_places=2)
    poignee = models.DecimalField(max_digits=10, decimal_places=2)
    cheville = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    materiaux_choices  = [
    ('Or massif 14k', 'Or massif 14k'),
    ('Or massif 10k', 'Or massif 10k'),
    ('Or rempli', 'Or rempli'),
    ('Argent sterling', 'Argent sterling'),]
    materiaux=models.CharField(choices=materiaux_choices, max_length=50,default='Non defini')
    numero=models.IntegerField(null=True,unique=True)
    def __str__(self):
        return self.name
    

