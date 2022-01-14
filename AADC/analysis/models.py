from django.db import models
from django.db.models import Model
# Create your models here.

class Graphic(Model):
    imageGraphic = models.ImageField()
    objetos  =  models.Manager()