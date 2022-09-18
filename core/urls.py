from django.urls import path
from .views import CarteiraIndex

urlpatterns = [
    path('', CarteiraIndex.as_view(), name='index')
]