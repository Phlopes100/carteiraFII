from asyncio import run_coroutine_threadsafe
from unicodedata import decimal
import requests
from django.shortcuts import HttpResponse
from bs4 import BeautifulSoup
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.models import Carteira
from django.urls import reverse_lazy

# Create your views here.


class CarteiraIndex(ListView):
    template_name = 'core/index.html'
    model = Carteira
    
   
    def get_context_data(self, **kwargs):
        dados = []
        data = Carteira.objects.all()
        HEADER = {'User agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
        for cota in data:
            url = f'https://statusinvest.com.br/fundos-imobiliarios/{cota.nome_cota}'
            response = requests.get(url, headers=HEADER)
        
            if response.status_code == 200:
                print("Opa deu certo...")
                soup = BeautifulSoup(response.content, 'html.parser')
                valor_cota_atual = soup.find('strong', class_="value").text.replace(',','.')
                ultimo_pg = soup.find('strong', class_="value d-inline-block fs-5 fw-900").text.replace(',','.')
                ul_pg = float(ultimo_pg)
                vl_ct_at = float(valor_cota_atual)
                porcentagem_pg = (ul_pg / vl_ct_at) * 100
                rendimento_mensal = round(ul_pg * cota.quantidade_cota, 2)
                rendimento_semestral = round(rendimento_mensal * 6, 2)
                rendimento_anual = round(rendimento_mensal * 12, 2)
                qt_cp_cota_mensal = round(rendimento_mensal / vl_ct_at)
                qt_cp_cota_semestral = round(rendimento_semestral / vl_ct_at)
                qt_cp_cota_anual = round(rendimento_anual / vl_ct_at)
                print(f'Nome Cota: {cota.nome_cota}')
                print(f'Quantidade: {cota.quantidade_cota}')
                print(f'Valor cotal atual: {vl_ct_at}')
                print(f'Último pagamento: {ul_pg}')
                print(f'Porcentagem %: {porcentagem_pg}')
                print(f'Rendimento Mensal: {rendimento_mensal}')
                print(f'Rendimento Semestral: {rendimento_semestral}')
                print(f'Rendimento Anual: {rendimento_anual}\n')

                meu_dic = {
                    'id': cota.id,
                    'cota': cota.nome_cota,
                    'quantidade': cota.quantidade_cota,
                    'ultimo_pagamento': round(ul_pg, 2),
                    'valor_cota_atual': vl_ct_at,
                    'porcentagem': round(porcentagem_pg, 2),
                    'sg_mensal': qt_cp_cota_mensal,
                    'sg_semestral': qt_cp_cota_semestral,
                    'sg_anual': qt_cp_cota_anual,
                    'rendimento_mensal': rendimento_mensal,
                    'rendimento_semestral': rendimento_semestral,
                    'rendimento_anual': rendimento_anual,
                }
                dados.append(meu_dic)
            else:
                print("Ocorreu um erro")
        
        
        quantidade = []
        mensal = []
        semestral = []
        anual = []
        sg_mensal = []
        sg_semestral = []
        sg_anual = []
 
        for d in dados:
            quantidade.append(d['quantidade'])
            mensal.append(d['rendimento_mensal'])
            semestral.append(d['rendimento_semestral'])
            anual.append(d['rendimento_anual'])
            sg_mensal.append(d['sg_mensal'])
            sg_semestral.append(d['sg_semestral'])
            sg_anual.append(d['sg_anual'])

        total_quantidade = sum(quantidade)
        total_mensal = sum(mensal)
        total_sg_mensal = sum(sg_mensal)
        total_sg_semestral = sum(sg_semestral)
        total_sg_anual = sum(sg_anual)
        total_semestral = sum(semestral)
        total_anual = sum(anual)

        data = super().get_context_data(**kwargs)
        data['resultados'] = dados
        data['total_cotas'] = total_quantidade
        data['total_mensal'] = round(total_mensal, 2)
        data['total_semestral'] = round(total_semestral, 2)
        data['total_anual'] = round(total_anual, 2)
        data['total_sg_mensal'] = total_sg_mensal
        data['total_sg_semestral'] = total_sg_semestral
        data['total_sg_anual'] = total_sg_anual
        return data


class CarteiraCreate(CreateView):
    template_name = 'core/adicionar_cota.html'
    model = Carteira
    fields = '__all__'
    success_url = reverse_lazy('index')


class CarteiraUpdate(UpdateView):
    template_name = 'core/atualizar_cota.html'
    model = Carteira
    fields = '__all__'
    success_url = reverse_lazy('index')


class CarteiraDelete(DeleteView):
    template_name = 'core/deletar_cota.html'
    model = Carteira
    success_url = reverse_lazy('index')


