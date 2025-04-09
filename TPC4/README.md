# Analisador Léxico SPARQL

Este projeto implementa um **analisador léxico** para uma linguagem de queries semelhante ao **SPARQL**, utilizando a biblioteca `PLY` (Python Lex-Yacc).

## 📄 Objetivo

O objetivo do programa é processar uma query SPARQL e dividir o texto de entrada em **tokens léxicos** que representam os componentes da linguagem, tais como variáveis, URIs, literais, palavras-chave (`select`, `where`, `LIMIT`), entre outros.

## ⚙️ Como funciona

- O programa usa a biblioteca `ply.lex` para definir expressões regulares que identificam diferentes tipos de tokens.
- Cada token é definido por uma função (`t_TOKENNAME`) ou por uma expressão direta (como `t_DOT`, `t_LBRACE`, etc.).
- O texto de entrada (`data`) é uma query SPARQL simples, que será lida e analisada pelo lexer.
- Os tokens detetados são impressos no ecrã com o seu tipo, valor e posição.

## 🧠 Tokens suportados

| Token     | Descrição                                 | Exemplo                          |
|-----------|-------------------------------------------|----------------------------------|
| SELECT    | Palavra-chave `select`                    | `select`                         |
| WHERE     | Palavra-chave `where`                     | `where`                          |
| LIMIT     | Palavra-chave `LIMIT`                     | `LIMIT`                          |
| RDFTYPE   | Palavra-chave `a`                         | `a` (representa `rdf:type`)      |
| QMARK     | Variáveis SPARQL                          | `?nome`, `?s`, `?desc`           |
| ID        | URIs abreviadas                           | `dbo:MusicalArtist`, `foaf:name` |
| STRING    | Literais com ou sem idioma                | `"Chuck Berry"@en`               |
| NUMBER    | Números inteiros                          | `1000`                           |
| DOT       | Símbolo de fim de instrução               | `.`                              |
| EQUALS    | Sinal de igual (não usado no exemplo)     | `=`                              |
| LBRACE    | Abertura de bloco                         | `{`                              |
| RBRACE    | Fecho de bloco                            | `}`                              |

## 📌 Notas importantes

- O programa ignora comentários iniciados por `#`.
- Também ignora espaços em branco e tabulações (`\t`).
- Erros de caracteres não reconhecidos são reportados no terminal.

