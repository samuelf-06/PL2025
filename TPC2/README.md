# Análise de um dataset de obras musicais

Este programa processa um ficheiro `obras.csv` com registos de obras musicais, utilizando **expressões regulares** para extrair e organizar a informação, sem usar o módulo `csv`.

## Objetivos

- Contar compositores únicos
- Contar obras por período
- Listar títulos organizados por período

## Etapas

1. **Limpeza do CSV**
   - Remove quebras de linha internas nos campos e guarda em `obras_formatado.csv`.

2. **Extração com regex**
   - Compositores: `;\d\d\d\d;.*?;(.*?);`
   - Períodos: `;\d\d\d\d;(.+?);`
   - Título e período: `(.+);".+";\d\d\d\d;(.+?);`

3. **Organização dos dados**
   - Usa `set` para compositores únicos.
   - Usa `dict` para contar obras por período e agrupar títulos.

4. **Apresentação**
   - Imprime os dados de forma legível no terminal.

## Exemplo de Saída

Número total de compositores: 58 Compositores: ['Bach', 'Beethoven', ...]

Número de obras por período: Barroco: 23 Romântico: 45 ...

Títulos organizados por período: Romântico (45 obras):

Noturno Op. 9 n.º 2