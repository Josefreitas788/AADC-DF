import urllib.request
import urllib.parse
import html

def decode_texto(texto):
    #texto = texto.replace("\xc1", "Á")
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
    url = 'https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm'
    values = {'relaxation':cep, 'tipoCEP': 'ALL'}

    request = urllib.request.Request(url, urllib.parse.urlencode(values).encode())
    result = urllib.request.urlopen(request).read()
    result = str(result)

    try:
        inicio = int(result.index('CEP:</th>') + len('CEP:</th>'))
        fim = int(result.index('<td width="55">'))

        resultado = result[ inicio : fim ]

        resultado = html.unescape(resultado)
        resultado = decode_texto(resultado)

        print(resultado)

    except ValueError: 
        print('Indefinido')
