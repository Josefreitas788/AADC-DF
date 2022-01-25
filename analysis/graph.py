from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
import matplotlib.pyplot as plt
from IPython.display import display
import io, os
import urllib, base64
import gdown
from analysis.models import Graphic

#from cep_df import cep_df

# Checa se existe os dados em .csv
arquivo_csv = "AADC/csv/Covid_DF.csv"
if not os.path.isfile(arquivo_csv):
    os.makedirs("AADC/csv", exist_ok=True)
    gdown.download("https://drive.google.com/u/0/uc?id=1vKiEsNMtWXLhK9h9Og2VpzXEonQOIfas", arquivo_csv, quiet=False)

dados = pd.read_csv(arquivo_csv, sep = ';')

# Colunas Selecionadas
colunas_selecionadas =  ['paciente_idade', 'paciente_enumsexobiologico', 'paciente_racacor_valor', 'paciente_endereco_nmmunicipio', 'paciente_endereco_nmpais', 'paciente_endereco_uf', 'estalecimento_nofantasia', 'vacina_grupoatendimento_nome', 'vacina_categoria_nome', 'vacina_descricao_dose', 'vacina_nome', 'paciente_endereco_cep']

# Novo Dataframe com as colunas selecionadas
dados_vacina = dados.filter(items = colunas_selecionadas)

# Idades inconsistentes foram substituidas pela média aritmética da coluna 'paciente_idade'
dados_vacina.loc[dados_vacina['paciente_idade'].isnull()] = dados_vacina['paciente_idade'].mean()

# Dados nulos das outras colunas foram substituidos por 'Não informado'
dados_vacina.fillna("Não informado", inplace = True)

# Soma de valores nulos em cada coluna
#print(dados_vacina.isnull().sum())

# Drop paciente_racacor_valor = 50.59404737212269]
dados_vacina.drop(dados_vacina.loc[dados_vacina['paciente_racacor_valor'] == 50.59404737212269].index, inplace=True)

#Alteração na UF do paciente
dados_vacina.loc[dados_vacina['paciente_endereco_uf'] == 'XX'] = 'Não informado'

####################### Quantidade de pessoas que tomaram a 1°, 2° e 3° dose #######################

def graf_quant_dose123():
    # Filtrando dados do DataFrame
    colunas = ['vacina_descricao_dose']
    doses = dados_vacina.filter(items=colunas)
 
    graf = doses.value_counts()

    labels = ['1° Dose', '2° Dose', 'Dose única','Não informado' ]
    plt.style.use("ggplot")
    explode = (0.1, 0.0, 0.0, 0.0)

    labels1 = ['', '', '', '']
    graf.plot.pie(autopct='%1.1f%%', shadow=True, startangle = 90, ylabel='', title = 'Porcentagem de pessoas que tomaram a 1° dose, 2° dose e a dose única.\n', subplots=True, labels = labels1,explode= explode ) 

    L = plt.legend( bbox_to_anchor=(1, 0, 0.5, 1), loc='center left', labels = labels)
    #plt.show() 

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

#######################Classificação por região geográfica.(estados do Brasil)#######################

def graf_regiao_geografica_estados():

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_uf']
    dados_regiao_geografica = dados_vacina.filter(items=colunas)

    # Gráfico UF do paciente 
    graf = (dados_regiao_geografica['paciente_endereco_uf'].value_counts())

    graf.plot.bar(title = 'Localização geográfica das pessoas que se vacinaram no DF\n', xlabel= 'Estados', ylabel = 'Quantidade de pessoas')
    #plt.show() 

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


####################### Classificação por região geográfica. (paises) #######################

def graf_regiao_geografica_paises():

    label = 'Ruanda', 'Venezuela', 'Bolívia' ,  'Congo', 'Japão', 'Andorra','Colômbia', 'Gibraltar', 'Portugal', 'São Tomé e Príncipe'

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_nmpais']
    regiao_geografica_paises = dados_vacina.filter(items=colunas)

    # Gráfico país do paciente 
    graf_paises = (regiao_geografica_paises['paciente_endereco_nmpais'].value_counts())

    # Países estrangeiros 
    graf_paises_estrangeiros = regiao_geografica_paises[(regiao_geografica_paises['paciente_endereco_nmpais'] != 'BRASIL') & (regiao_geografica_paises['paciente_endereco_nmpais'] != 'Não informado')].value_counts()

    # Criação do gráfico
    fig, axs = plt.subplots(1,2)
    axs[0].set_title('Países')
    axs[0].pie(graf_paises, shadow=True, startangle=90)
    axs[1].set_title('Países estrangeiros')
    axs[1].pie(graf_paises_estrangeiros, labels=label, shadow=True, startangle=90)
  
    #Django
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

####################### Faixa etária das pessoas que tomaram a vacina. #######################

def faixa_etaria():

  # Filtrando dados do DataFrame
    colunas = ['paciente_idade']
    idade = dados_vacina.filter(items=colunas)
    #idade = dados_vacina['paciente_idade']
 
    # Alteração na idade  do paciente
    idade.drop(idade.loc[idade['paciente_idade'] == 'Não informado'].index, inplace=True)
    
    # Criação do gráfico
    
    idade.plot.hist(bins=30,color= 'green') 

    #Django
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri    

####################### Classificação por vacina (Pfizer..) #######################
def name_vacina():
    # Filtrando dados do DataFrame
    colunas = ['vacina_nome']
    vacinas = dados_vacina['vacina_nome']

    vacinas = vacinas.replace('Vacina Covid-19 - Covishield', 'Covishield')
    vacinas = vacinas.replace('Covid-19-Coronavac-Sinovac/Butantan', 'Sinovac/Butantan')
    vacinas = vacinas.replace('Vacina covid-19 - BNT162b2 - BioNTech/Fosun Pharma/Pfizer', 'Pfizer')
    vacinas = vacinas.replace('Covid-19-AstraZeneca', 'AstraZeneca')
    vacinas = vacinas.replace('Vacina covid-19 - Ad26.COV2.S - Janssen-Cilag', 'Janssen-Cilag')

    # Gráfico
    graf = vacinas.value_counts()
    graf.plot.bar(title='Vacinas utilizadas x Quantidade')
    #print(graf)

    #Django
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri



####################### Classificação por Etnia #######################
def vacina_etnia():
    #Filtrando as colunas
    dados_limpos = dados[ dados['paciente_racacor_valor'] == 'SEM INFORMACAO' ].index
    dados.drop(dados_limpos , inplace=True)
    graf = (dados['paciente_racacor_valor'].value_counts())
    #Criando o grafico
    graf.plot.bar(title = 'Etnia\n',xlabel= 'Vacinas', ylabel = 'Frequência', color= "ORANGE")

    #Django
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri    
####################### Classificação por Grupo de vacinados #######################

def vacina_categoria():
    #Filtrando as colunas
    graf = (dados['vacina_categoria_nome'].value_counts())
    #Criando o grafico
    graf.plot.bar(title = 'Categorias mais vacinadas no DF\n', xlabel= 'Vacinas', ylabel = 'Frequência', color = "green")

    #Django
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri    
####################### Classificação por genero biologico #######################

def vacina_genero_biologico():
    #Fltrando coluna
    graf = (dados['paciente_enumsexobiologico'].value_counts())
    #Criando o grafico
    graf.plot.pie(title = 'Gênero que mais se vacinou no  DF\n', autopct='%1.1f%%',xlabel= 'Vacinas', ylabel = 'Porcentagem')

    #Django
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri    
####################### Classificação por UF dos vacinados #######################
def uf_dos_vacinados():
    #Fltrando coluna
    graf = (dados['paciente_endereco_uf'].value_counts())
    #Criando o grafico
    graf.plot.bar(title = 'UF dos pacientes que foram vacinados no DF\n', xlabel= 'Vacinas', ylabel = 'Frequência', color = "Yellow")

    #Django
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri    
####################### Classificação das doses ja tomadas #######################
def dose_tomada():
    #Filtrando as colunas
    graf = (dados['vacina_descricao_dose'].value_counts())
    #Criando os graficos
    graf.plot.barh(title = 'Quantidade das doses já tomadas DF\n', xlabel= 'Vacinas', ylabel = 'Frequência', color="purple")

    #Django
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri  

# Chamando as funções 
Quantidade_doses = Graphic(imageGraphic = graf_quant_dose123())
Quantidade_doses.save()
Região_geografica_estados = Graphic(imageGraphic = graf_regiao_geografica_estados())
Região_geografica_estados.save()
Região_geografica_paises = Graphic(imageGraphic = graf_regiao_geografica_paises())
Região_geografica_paises.save()
Faixa_Etaria = Graphic(imageGraphic = faixa_etaria())
Faixa_Etaria.save()
Nome_vacina = Graphic(imageGraphic = name_vacina())
Nome_vacina.save()
Vacina_etnia = Graphic(imageGraphic = vacina_etnia())
Vacina_etnia.save()
Vacina_Categoria = Graphic(imageGraphic = vacina_categoria())
Vacina_Categoria.save()
Vacina_Genero = Graphic(imageGraphic = vacina_genero_biologico())
Vacina_Genero.save()
Uf_Vacinados = Graphic(imageGraphic = uf_dos_vacinados())
Uf_Vacinados.save()
Dose_Tomada = Graphic(imageGraphic = dose_tomada())
Dose_Tomada.save()






#graf_regiao_geografica_df()
#exportar_dados()
