# Conversor de Markdown para HTML

Este script em Python converte um ficheiro `.md` (Markdown) para HTML, processando os seguintes elementos:

## ✅ Funcionalidades

O script reconhece e converte:

- **Cabeçalhos** (`#`, `##`, `###`, ..., `######`)
  - Exemplo: `## Título` → `<h2>Título</h2>`
- **Texto em Negrito** (`**texto**`)
  - Exemplo: `**importante**` → `<b>importante</b>`
- **Texto em Itálico** (`*texto*`)
  - Exemplo: `*ênfase*` → `<i>ênfase</i>`
- **Listas numeradas**
  - Exemplo:
    ```
    1. Item um
    2. Item dois
    ```
    converte para:
    ```html
    <ol>
      <li>Item um</li>
      <li>Item dois</li>
    </ol>
    ```
- **Links** no formato `[texto](URL)`
  - Exemplo: `[Google](http://google.com)` → `<a href="http://google.com">Google</a>`
- **Imagens** no formato `![alt](URL)`
  - Exemplo: `![coelho](http://imagem.com/coelho.jpg)` → `<img src="http://imagem.com/coelho.jpg" alt="coelho"/>`

## 🧠 Como funciona

1. **Lê o ficheiro `EXEMPLO.md` linha a linha**
2. Usa **expressões regulares (regex)** para detetar padrões Markdown
3. Substitui cada padrão pelo respetivo HTML
4. Imprime o resultado convertido no terminal (podes redirecionar para um ficheiro se quiseres)

## 🏁 Como correr

1. Coloca o conteúdo Markdown que queres converter no ficheiro `EXEMPLO.md`
2. Corre o script Python
