from . import views 
 
app_name = 'analysis' 
 
# urlpatterns contém a lista de roteamentos de URLs 
urlpatterns = [ 
  # GET / 
  path('', views.index, name='index'), 
] 