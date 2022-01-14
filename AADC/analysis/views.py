from django.shortcuts import render
from django.views.generic import ListView
from analysis.models import Graphic
#from . import graph

class Graphic_list(ListView):

    template_name = "templates/index.html" 
    model = Graphic 
    context_object_name = "Graphic"



