from django.contrib import admin
from .models import Carteira
# Register your models here.

@admin.register(Carteira)
class CarteiraAdmin(admin.ModelAdmin):
    list_display = ['nome_cota', 'quantidade_cota']
