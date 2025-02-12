# TPC1 - Calculadora de Soma

Este é um simples script em Python que atua como uma calculadora de soma, processando um texto para encontrar sequências de números e realizar operações de soma com base em comandos 'on' e 'off'.

## Funcionamento do Código

- **Inicialização das Variáveis**: 
  - A variável 'somador' é inicializada como True para indicar que a soma está ativa inicialmente.
  - 'total' é inicializada com um valor de 0.

- **Padrão Regex**:
  - O script compila um padrão regex para encontrar números, 'on', 'off' e '=' no texto fornecido.

- **Iteração sobre Correspondências**:
  - Itera sobre as correspondências encontradas no texto.
  - Para cada correspondência, verifica o tipo de comando:
    - Se for 'on', ativa a soma.
    - Se for 'off', desativa a soma.
    - Se for um número e a soma estiver ativa, adiciona-o à soma atual.
    - Se for '=', imprime a soma atual.
