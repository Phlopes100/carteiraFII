from django.urls import path
from .views import CarteiraCreate, CarteiraDelete, CarteiraIndex, CarteiraUpdate

urlpatterns = [
    path('', CarteiraIndex.as_view(), name='index'),
    path('adicionar/', CarteiraCreate.as_view(), name="adicionar_cota"),
    path('atualizar/<int:pk>/', CarteiraUpdate.as_view(), name="atualizar_cota"),
    path('deletar/<int:pk>/', CarteiraDelete.as_view(), name="deletar_cota"),

]