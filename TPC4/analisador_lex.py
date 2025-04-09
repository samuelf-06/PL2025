import ply.lex as lex

tokens = ['STRING', 'ID', 'NUMBER', 'DOT', 'EQUALS', 'QMARK', 
          'LBRACE', 'RBRACE', 'SELECT', 'WHERE', 'LIMIT', 'RDFTYPE']

t_SELECT = r'select'
t_WHERE = r'where'
t_LIMIT = r'LIMIT'

def t_QMARK(t):
    r'\?\w+'
    return t

def t_ID(t):
    r'[a-zA-Z_]\w*:[a-zA-Z_]\w*'
    return t

def t_STRING(t):
    r'"[^"]*"(?:@[a-zA-Z_]+)?'
    return t

def t_NUMBER(t): 
    r'\d+'
    t.value = int(t.value)
    return t

def t_RDFTYPE(t):
    r'a'
    return t

t_DOT = r'\.'
t_EQUALS = r'\='
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_ignore = ' \t'

def t_comments(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter Ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

data = '''
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
'''

lexer.input(data)

print("Results")
for token in lexer:
    print(token)
    
