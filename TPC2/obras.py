import re

def formatar_csv(inputFile, outputFile):
# Lê o conteúdo do ficheiro CSV
    with open(inputFile, 'r', encoding='utf-8') as input, open(outputFile, 'w', encoding='utf-8') as output:
        conteudo = input.read()
        formatar = re.sub(r'\n\s+', ' ', conteudo)
        output.write(formatar)

formatar_csv('obras.csv', 'obras_formatado.csv')

with open('obras_formatado.csv', 'r', encoding='utf-8') as f:
    conteudo = f.readlines()

# Inicialização
compositores = set()
compositor = r';\d\d\d\d;.*?;(.*?);'
periodo_contagem = {}
periodo = r';\d\d\d\d;(.+?);'
dicionario = {}
titulo_periodo = r'(.+);".+";\d\d\d\d;(.+?);'

# Processamento de cada registo
for linha in conteudo:
    if "nome" in linha:
        continue
    m = re.search(compositor, linha)
    if m:
        compositores.add(m.group(1))

for linha in conteudo:
    if "periodo" in linha:
        continue
    m = re.search(periodo, linha)
    if m:
        if m.group(1) in periodo_contagem:
            periodo_contagem[m.group(1)] += 1
        else:
            periodo_contagem[m.group(1)] = 1

for linha in conteudo:
    if "titulo" in linha:
        continue
    m = re.search(titulo_periodo, linha)
    if m:
        periodo = m.group(2)
        titulo = m.group(1)
        if periodo in dicionario:
            dicionario[periodo].append(titulo)
        else:
            dicionario[periodo] = [titulo]

# Output
print(f"\nNúmero total de compositores: {len(compositores)}")
print(f"Compositores: {sorted(compositores)}")

print("\nNúmero de obras por período:")
for p, c in periodo_contagem.items():
    print(f"  {p}: {c}")

print("\nTítulos organizados por período:")
for periodo, titulos in dicionario.items():
    print(f"\n{periodo} ({len(titulos)} obras):")
    for t in titulos:
        print(f"  - {t}")
