import pandas as pd 
import matplotlib.pyplot as plt
from IPython.display import display
from cep_df import cep_df

# Importando os dados
# add o caminho dos dados 
dados = pd.read_csv('D:\heloh\Documents\Faculdade\Covid_DF.csv', sep = ';')


# Colunas Selecionadas
colunas_selecionadas =  ['paciente_idade', 'paciente_enumsexobiologico', 'paciente_racacor_valor', 'paciente_endereco_nmmunicipio', 'paciente_endereco_nmpais', 'paciente_endereco_uf', 'paciente_nacionalidade_enumnacionalidade', 'estalecimento_nofantasia', 'vacina_grupoatendimento_nome', 'vacina_categoria_nome', 'vacina_descricao_dose', 'vacina_nome', 'paciente_endereco_cep']

# Excluir = paciente_nacionalidade_enumnacionalidade 

# Novo Dataframe com as colunas selecionadas 
dados_vacina = dados.filter(items = colunas_selecionadas)

# Idades inconsistentes foram substituidas pela média aritmética da coluna 'paciente_idade'
dados_vacina.loc[dados_vacina['paciente_idade'].isnull()] = dados_vacina['paciente_idade'].mean()

# Dados nulos das outras colunas foram substituidos por 'Não informado' 
dados_vacina.fillna("Não informado", inplace = True)

# Soma de valores nulos em cada coluna
print(dados_vacina.isnull().sum())

# Drop paciente_racacor_valor = 50.59404737212269]
#print((dados_vacina['paciente_racacor_valor']).value_counts())
#print(dados_vacina.loc[dados_vacina['paciente_racacor_valor'] == 50.59404737212269] )
dados_vacina.drop(dados_vacina.loc[dados_vacina['paciente_racacor_valor'] == 50.59404737212269].index, inplace=True)

#Alteração na UF do paciente
dados_vacina.loc[dados_vacina['paciente_endereco_uf'] == 'XX'] = 'Não informado'

# Exportando dados
#dados_vacina.to_csv('dados_vacina.csv')


# Quantidade de pessoas que tomaram a 1°, 2° e 3° dose
def graf_quant_dose123():

    # Filtrando dados do DataFrame
    colunas = ['vacina_descricao_dose']
    doses = dados_vacina.filter(items=colunas)
 
    graf = doses.value_counts()

    labels = ['1° Dose', '2° Dose', 'Dose única']
    plt.style.use("ggplot")
    explode = (0.1, 0.0, 0.0)
    
    graf.plot.pie(autopct='%1.1f%%', explode = explode, shadow=True, startangle = 90, ylabel='', title = 'Porcentagem de pessoas que tomaram a 1° dose, 2° dose e a dose única.\n', subplots=True, labels = ['', '', '']) 

    L = plt.legend( bbox_to_anchor=(1, 0, 0.5, 1), loc='center left', labels = labels)
    plt.show() 


# Classificação por região geográfica.
def graf_regiao_geografica_brasil ():

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_cep', 'paciente_endereco_nmmunicipio', 'paciente_endereco_uf']
    dados_regiao_geografica = dados_vacina.filter(items=colunas)

    # Gráfico UF do paciente | falta terminar
    #graf = dados_vacina['paciente_endereco_uf'].value_counts()
    graf = dados_vacina.groupby('paciente_endereco_uf').count()
    #print(graf)
    graf.plot.barh()
    plt.show() 

def graf_regiao_geografica_df ():

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_cep', 'paciente_endereco_nmmunicipio', 'paciente_endereco_uf']
    dados_regiao_geografica_df = dados_vacina.filter(items=colunas)

    dados_regiao_geografica_df = dados_regiao_geografica_df[dados_regiao_geografica_df.paciente_endereco_uf == 'DF']

    #for i in dados_regiao_geografica_df['paciente_endereco_cep']:
    #    dados_regiao_geografica_df['RA'] = cep_df(i)

    '''
    list_cep = []
    for i in dados_regiao_geografica_df.paciente_endereco_cep:
        list_cep.append(cep_df(i))
        print(cep_df(i))
    '''
    

    dados_regiao_geografica_df['RA'] = [cep_df(cep) for cep in dados_regiao_geografica_df.paciente_endereco_cep]

    #dados_regiao_geografica_df['RA'] = cep_df(dados_regiao_geografica_df['paciente_endereco_cep'])
    '''
    tt = dados_regiao_geografica_df['paciente_endereco_cep'][0]
    print(tt)
    print(cep_df(tt))
    '''

    print(dados_regiao_geografica_df)




# Chamando as funções 
#graf_quant_dose123()
#graf_regiao_geografica()
graf_regiao_geografica_df()