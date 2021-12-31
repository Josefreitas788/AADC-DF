import pandas as pd 
import matplotlib.pyplot as plt
from IPython.display import display

# Importando os dados
# add o caminho dos dados 
dados = pd.read_csv('#', sep = ';')

# Colunas Selecionadas
colunas_selecionadas =  ['paciente_idade', 'paciente_enumsexobiologico', 'paciente_racacor_valor', 'paciente_endereco_nmmunicipio', 'paciente_endereco_nmpais', 'paciente_endereco_uf', 'paciente_nacionalidade_enumnacionalidade', 'estalecimento_nofantasia', 'vacina_grupoatendimento_nome', 'vacina_categoria_nome', 'vacina_descricao_dose', 'vacina_nome' ]

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

# Exportando dados
#dados_vacina.to_csv('dados_vacina.csv')


# Quantidade de pessoas que tomaram a 1°, 2° e 3° dose
def quant_dose123():

    coluna_descricao_dose = dados_vacina['vacina_descricao_dose']
    
    doses = coluna_descricao_dose.value_counts()
    labels = ['1° Dose', '2° Dose', 'Dose única']
    plt.style.use("ggplot")
    explode = (0.1, 0.0, 0.0)
    
    doses.plot.pie(autopct='%1.1f%%', explode = explode, shadow=True, startangle = 90, ylabel='', title = 'Porcentagem de pessoas que tomaram a 1° dose, 2° dose e a dose única.\n', subplots=True, labels = ['', '', '']) 

    L = plt.legend( bbox_to_anchor=(1, 0, 0.5, 1), loc='center left', labels = labels)
    plt.show() 
    
quant_dose123()