from django.db import models

# Create your models here.
class Carteira(models.Model):
    nome_cota = models.CharField(max_length=10)
    quantidade_cota = models.IntegerField()
    