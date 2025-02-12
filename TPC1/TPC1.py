import re
import fileinput

stdin = "\n".join(fileinput.input())
contas = r'(on|off|=|\d+)'

simbolos = re.findall(contas, stdin, flags=re.IGNORECASE)
somador = True
total = 0

for simbolo in simbolos:
    if simbolo.lower() == 'on':
        somador = True
    elif simbolo.lower() == 'off': 
        somador = False
    elif simbolo == '=':
        print("Total:", total)
    elif simbolo.isdigit() and somador:
        total += int(simbolo)