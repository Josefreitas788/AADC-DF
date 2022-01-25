from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
import matplotlib.pyplot as plt
from IPython.display import display
import io, os
import urllib, base64
import gdown
from analysis import graph

def index(request):
    graphics = []
    graphic_id = ['graf_quant_dose', 'graf_estados', 'graf_paises', 'graf_faixa_etaria', 'graf_nome_vacina',
    'graf_dose_tomada', 'graf_vacina_etnia', 'graf_vacina_categoria', 'graf_vacina_genero_biologico', 'graf_uf_vacinados']
    for graph in graphic_id:
        graphics.append(f"img/{graph}.png")
    context = {
        'graphics': graphics,
        'graphic_id': graphic_id,
        'total_cases': 0,
        'total_deaths': 0,
        'total_recovered': 0,
    }
    return render(request, 'index.html', context)
