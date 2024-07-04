from django.db import models
from math import floor
from .constances import constances as c
import datetime, uuid
from django.utils import timezone


# Create your models here.
class Token(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    email = models.CharField(max_length=100,null=False)
    password = models.CharField(max_length=100,null=False)
    now=floor(datetime.datetime.now().timestamp())
    creation_date = models.IntegerField(default=now)
    
    class Meta:
        ordering =["creation_date"]

    def __str__(self):
        return self.id
        
# Create your models here.
class Session(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    email = models.CharField(max_length=200)
    access = models.CharField(max_length=300,default='')
    refresh = models.CharField(max_length=300,default='')
    ip = models.CharField(max_length=1000,default='')
    now=floor(datetime.datetime.now().timestamp())
    end_time = models.IntegerField(default=(now + (3600*24*30)))
    creation_date = models.IntegerField(default=now)
    
    class Meta:
        ordering =["creation_date"]

    def __str__(self):
        return self.id

# Create your models here.
class Entite(models.Model):
    id = models.CharField(primary_key=True,unique=True,max_length=100)
    email = models.CharField(max_length=100,unique=True)
    nom = models.CharField(max_length=200)
    photo = models.CharField(max_length=200)
    adresse = models.CharField(max_length=100)
    statut = models.CharField(max_length=200,default='1') # les differents statuts"créé(1), validé(2), effacé(5). 
    description = models.CharField(max_length=2000)
    telephone = models.CharField(max_length=200)
    now=floor(datetime.datetime.now().timestamp())
    creation_date = models.IntegerField(default=now)
    
    class Meta:
        ordering =["creation_date"]

    def __str__(self):
        return self.id

# Create your models here.
class Client(models.Model):
    id = models.CharField(primary_key=True,unique=True,max_length=100)
    nom = models.CharField(max_length=100,default='',null=False)
    prenom = models.CharField(max_length=100,default='')
    email = models.CharField(max_length=100,unique=True)
    photo = models.CharField(max_length=200)
    sexe = models.CharField(max_length=100)
    statut = models.CharField(max_length=200,default='1') # les differents statuts"créé(1), validé(2), effacé(5). 
    cni = models.CharField(max_length=200,default='')
    telephone = models.CharField(max_length=200)
    now=floor(datetime.datetime.now().timestamp())
    creation_date = models.IntegerField(default=now)
    
    class Meta:
        ordering =["creation_date"]

    def __str__(self):
        return self.id
    # create your models here.
class Admin(models.Model):
    id = models.CharField(primary_key=True,unique=True,max_length=100)
    id_entite = models.CharField(max_length=100,null=False)
    nom = models.CharField(max_length=100,default='')
    prenom = models.CharField(max_length=100,default='')
    email = models.CharField(max_length=100,unique=True)
    photo = models.CharField(max_length=200)
    now=floor(datetime.datetime.now().timestamp())
    creation_date = models.IntegerField(default=now)
    
    class Meta:
        ordering =["creation_date"]

    def __str__(self):
        return self.id
     # create your models here.
class Superadmin(models.Model):
    id = models.CharField(primary_key=True,unique=True,max_length=100)
    nom = models.CharField(max_length=100,default='')
    prenom = models.CharField(max_length=100,default='')
    email = models.CharField(max_length=100,unique=True)
    now=floor(datetime.datetime.now().timestamp())
    creation_date = models.IntegerField(default=now)
    
    class Meta:
        ordering =["creation_date"]

    def __str__(self):
        return self.id
      # create your models here.
class Chambre(models.Model):
    id = models.CharField(primary_key=True,unique=True,max_length=100)
    capacite = models.IntegerField(default=0)
    nom = models.CharField(max_length=100)
    statut = models.CharField(max_length=200,default='1') # les differents statuts"créé(1), validé(2), effacé(5).
    prix = models.IntegerField(default=0)
    now=floor(datetime.datetime.now().timestamp())
    creation_date = models.IntegerField(default=now)
    
    class Meta:
        ordering =["creation_date"]

    def __str__(self):
        return self.id
     # create your models here.
class Reservation(models.Model):
    id = models.CharField(primary_key=True,unique=True,max_length=100)
    id_client = models.CharField(max_length=100)
    date_debut = models.IntegerField(default=0)
    date_fin = models.IntegerField(default=0)
    statut = models.CharField(max_length= 200,default='1') # les differents statuts"créé(1), validé(2), effacé(5).
    prix = models.IntegerField(default=0)
    items = models.CharField(max_length=200)
    now=floor(datetime.datetime.now().timestamp())
    creation_date = models.IntegerField(default=now)
    
    class Meta:
        ordering =["creation_date"]

    def __str__(self):
        return self.id
       # create your models here.
class Photo(models.Model):
    id = models.CharField(primary_key=True,unique=True,max_length=100)
    id_chambre = models.CharField(max_length=100)
    id_entite = models.CharField(max_length=100)
    statut = models.CharField(max_length=200,default='1') # les differents statuts"créé(1), validé(2), effacé(5).
    url= models.CharField(max_length=100)
    now=floor(datetime.datetime.now().timestamp())
    creation_date = models.IntegerField(default=now)
    
    class Meta:
        ordering =["creation_date"]

    def __str__(self):
        return self.id
    