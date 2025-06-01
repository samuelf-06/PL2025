import ply.lex as lex
import re

# Pascal não diferencia maiúsculas e minúsculas:
flags = re.IGNORECASE

# Lista de tokens:
tokens = [
    'PROGRAM', 'BEGIN', 'END', 'VAR', 'IF', 'THEN', 'ELSE', 'FUNCTION',
    'PROCEDURE', 'WRITELN', 'READLN', 'FOR', 'TO', 'DOWNTO', 'WHILE', 'DO',
    'DIV', 'MOD', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'ARRAY', 'OF',
    'TIPOVAR', 'TIPOSTRING',
    'ID', 'NUMBER', 'STRING',
    'ASSIGN', 'EQ', 'NEQ', 'LE', 'GE', 'LT', 'GT', 'DOTDOT'
]

# Literais:
literals = ['+', '-', '*', '/', ';', ',', ':', '(', ')', '[', ']', '.']

# Definição de tokens para as palavras reservadas
def t_PROGRAM(t):    r'program';    return t
def t_BEGIN(t):      r'begin';      return t
def t_END(t):        r'end';        return t
def t_VAR(t):        r'var';        return t
def t_IF(t):         r'if';         return t
def t_THEN(t):       r'then';       return t
def t_ELSE(t):       r'else';       return t
def t_FUNCTION(t):   r'function';   return t
def t_PROCEDURE(t):  r'procedure';  return t
def t_WRITELN(t):    r'writeln';    return t
def t_READLN(t):     r'readln';     return t
def t_FOR(t):        r'for';        return t
def t_TO(t):         r'to';         return t
def t_DOWNTO(t):     r'downto';     return t
def t_WHILE(t):      r'while';      return t
def t_DO(t):         r'do';         return t
def t_DIV(t):        r'div';        return t
def t_MOD(t):        r'mod';        return t
def t_AND(t):        r'and';        return t
def t_OR(t):         r'or';         return t
def t_NOT(t):        r'not';        return t
def t_TRUE(t):       r'true';       return t
def t_FALSE(t):      r'false';      return t
def t_ARRAY(t):      r'array';      return t
def t_OF(t):         r'of';         return t
def t_TIPOVAR(t):    r'integer|real|boolean'; return t
def t_TIPOSTRING(t): r'string';     return t

# Identificadores:
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    word = t.value.lower()
    if word in ('integer', 'real', 'boolean'):
        t.type = 'TIPOVAR'
    elif word == 'string':
        t.type = 'TIPOSTRING'
    return t

# Atribuição e operadores:
t_ASSIGN = r':='
t_EQ     = r'='
t_NEQ    = r'<>'
t_LE     = r'<='
t_GE     = r'>='
t_LT     = r'<'
t_GT     = r'>'
t_DOTDOT = r'\.\.'

t_ignore = ' \t'

# Comentários:
def t_COMMENT(t):
    r'\{[^}]*\}'
    pass

def t_COMMENT_LINE(t):
    r'//.*'
    pass

# Números:
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Strings entre apóstrofos:
def t_STRING(t):
    r'\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]
    return t

# Contagem de linhas:
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erro:
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Criar o lexer:
lexer = lex.lex()