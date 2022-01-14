from django.shortcuts import render
from django.views.generic.edit import CreateView
from . import graph

def Graphic_list(request): 
  # Primeiro, buscamos os funcionarios 
  graphic = Graphic.objetos.all() 
 
  # Incluímos no contexto 
  contexto = { 
    'Graphic': Graphic 
  } 
 
  # Retornamos o template para listar os funcionários 
  return render( 
    request,  
    "templates/index.html",  
    contexto 
  )

