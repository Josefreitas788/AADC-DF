from django.shortcuts import render



# Create your views here.
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