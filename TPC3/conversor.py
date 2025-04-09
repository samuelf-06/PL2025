import re

# Expressões regulares
negrito = r'\*\*(.*?)\*\*'
italico = r'\*(.*?)\*'
cabecalho = r'(#{1,6})\s(.+)'
lista = r'^\s*(\d+)\.\s*(.+)'
link = r'\[([^\]]*?)\]\(([^\)]*?)\)'
imagem = r'!\[([^\]]*?)\]\(([^\)]*?)\)'

# Lê o ficheiro de entrada
with open('EXEMPLO.md', 'r', encoding='utf-8') as f:
    linhas = f.readlines()

html = []
em_lista = False

for linha in linhas:
    linha = linha.rstrip()

    # Imagem (fazer antes de links para evitar interferência)
    linha = re.sub(imagem, r'<img src="\2" alt="\1"/>', linha)

    # Links
    linha = re.sub(link, r'<a href="\2">\1</a>', linha)

    # Negrito e Itálico (negrito primeiro)
    linha = re.sub(negrito, r'<b>\1</b>', linha)
    linha = re.sub(italico, r'<i>\1</i>', linha)

    # Cabeçalhos
    cabecalho_match = re.match(cabecalho, linha)
    if cabecalho_match:
        nivel = len(cabecalho_match.group(1))
        conteudo = cabecalho_match.group(2)
        html.append(f'<h{nivel}>{conteudo}</h{nivel}>')
        continue

    # Lista numerada
    lista_match = re.match(lista, linha)
    if lista_match:
        if not em_lista:
            html.append('<ol>')
            em_lista = True
        html.append(f'<li>{lista_match.group(2)}</li>')
        continue
    else:
        if em_lista:
            html.append('</ol>')
            em_lista = False

    # Linha normal (pode ser vazia)
    html.append(linha)

# Fecha a lista, se ainda estiver aberta
if em_lista:
    html.append('</ol>')

# Output final
for linha in html:
    print(linha)
