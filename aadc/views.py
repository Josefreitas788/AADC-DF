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
    'graf_dose_tomada', 'graf_vacina_etnia', 'graf_vacina_categoria', 'graf_vacina_genero_biologico']
    for graph in graphic_id:
        graphics.append(get_graphics(graph))
    context = {
        'graphics': graphics,
        'graphic_id': graphic_id,
        'total_cases': 0,
        'total_deaths': 0,
        'total_recovered': 0,
    }
    return render(request, 'index.html', context)

def get_graphics(type):
    if (type == "graf_quant_dose"):
        return graph.graf_quant_dose123()    
    elif (type == "graf_estados"):
        return graph.graf_regiao_geografica_estados()
    elif (type == "graf_paises"):
        return graph.graf_regiao_geografica_paises()
    elif (type == "graf_faixa_etaria"):
        return graph.faixa_etaria()
    elif (type == "graf_nome_vacina"):
        return graph.name_vacina()
    elif (type == "graf_dose_tomada"):
        return graph.dose_tomada()
    elif (type == "graf_vacina_etnia"):
        return graph.vacina_etnia()
    elif (type == "graf_vacina_categoria"):
        return graph.vacina_categoria()
    elif (type == "graf_vacina_genero_biologico"):
        return graph.vacina_genero_biologico()