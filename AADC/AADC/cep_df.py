import urllib.request
import urllib.parse
import html

# Função que tem como objetivo decodificar tags HTML e caracteres hex. 
# Retorna o texto decodificado  
def decode_texto(texto):
    texto = texto.replace('\\r','')
    texto = texto.replace('\\n', '')
    texto = texto.replace('</tr>', '')
    texto = texto.replace('<tr>', '')
    texto = texto.replace('\\xe1', 'á')
    texto = texto.replace('\\xc1', 'Á')
    texto = texto.replace('\\xed', 'í')
    texto = texto.replace('\\xe2', 'â')
    return texto

def cep_df(cep):
    # url do site dos Correios
    url = 'https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm'
    # recebe os CEPs
    values = {'relaxation':cep, 'tipoCEP': 'ALL'}

    # Procura o CEP 
    request = urllib.request.Request(url, urllib.parse.urlencode(values).encode())
    result = urllib.request.urlopen(request).read()
    result = str(result)

    # Organiza o resultado obtido 
    try:
        inicio = int(result.index('CEP:</th>') + len('CEP:</th>'))
        fim = int(result.index('<td width="55">'))

        resultado = result[ inicio : fim ]
        
        #Logradouro/Nome | Bairro/Distrito | Localidade/UF
        resultado = html.unescape(resultado)
        resultado = decode_texto(resultado)

        #Localidade/UF
        localidade = resultado[ len(resultado) - (resultado[::-1].find('>dt<')):len(resultado) - 5]
        return localidade

    except ValueError: 
        return 'Indefinido' 
