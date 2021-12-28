import pandas as pd 
import matplotlib.pyplot as plt

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
