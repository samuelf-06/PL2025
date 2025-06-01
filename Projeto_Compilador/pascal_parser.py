import ply.yacc as yacc
from pascal_lex import tokens
from ast_nodes import *

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE'),
    ('left', '+', '-'),
    ('left', '*', '/', 'DIV', 'MOD'),
    ('nonassoc', 'LOWER_THAN_ELSE'),
    ('nonassoc', 'ELSE'),
)

funcoes_embutidas = {
    "length": 1,         # comprimento de uma string ou array
    "ord": 1,            # devolve o código ASCII de um caractere
    "chr": 1,            # converte código ASCII para caractere
    "succ": 1,           # sucessor de um valor ordinal (ex: succ('a') → 'b')
    "pred": 1,           # antecessor de um valor ordinal
    "abs": 1,            # valor absoluto
    "sqr": 1,            # quadrado
    "sqrt": 1,           # raiz quadrada
    "round": 1,          # arredonda para inteiro
    "trunc": 1,          # parte inteira de um número real
    "frac": 1,           # parte fracionária de um número real
    "upcase": 1,         # converte caractere para maiúscula
    "lowercase": 1,      # converte caractere para minúscula (não standard, mas útil)
    "str": 1,            # converte valor para string
    "val": 1,            # converte string para valor
    "pos": 2,            # posição de substring numa string
    "copy": 3,           # extrai substring
    "concat": 2,         # concatena duas strings
    "insert": 3,         # insere uma string noutra (pouco comum em compiladores simples)
    "delete": 3          # remove substring de string
}

declared_variables = set()
declared_functions = {} 
semantic_errors = []

def p_programa(p):
    'programa : PROGRAM ID ";" declaracoes bloco_simples "."'

    declared_functions.update(funcoes_embutidas)

    globais, funcoes = p[4]

    # Mapear variáveis globais:
    global var_positions, next_var_index
    for var in globais:
        if var not in var_positions:
            var_positions[var] = next_var_index
            next_var_index += 1

    p[0] = ProgramNode(p[2], funcoes, p[5])



def p_comando_composto(p):
    'comando_composto : BEGIN comandos END'
    p[0] = CompoundNode(p[2])

def p_comandos(p):
    '''comandos : comandos comando_semi
                | comando_semi'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_comando_semi(p):
    '''comando_semi : comando ";"
                    | comando'''
    p[0] = p[1]

def p_bloco_simples(p):
    '''bloco_simples : BEGIN comandos END
                     | BEGIN declaracoes_variaveis comandos END'''
    if p.slice[2].type == 'comandos':
        p[0] = CompoundNode(p[2])
    else:
        p[0] = CompoundNode(p[3])

def p_declaracoes(p):
    '''declaracoes : declaracoes_variaveis declaracoes_subprogramas declaracoes_variaveis_opt
                   | declaracoes_subprogramas declaracoes_variaveis_opt
                   | declaracoes_variaveis declaracoes_subprogramas
                   | declaracoes_variaveis
                   | declaracoes_subprogramas
                   | empty'''
    vars_list = []
    funcs_list = []

    if len(p) == 2:
        if isinstance(p[1], list):
            if all(isinstance(f, (FunctionDeclNode, ProcedureDeclNode)) for f in p[1]):
                funcs_list = p[1]
            else:
                vars_list = p[1]
    elif len(p) == 3:
        if isinstance(p[1], list):
            if all(isinstance(f, (FunctionDeclNode, ProcedureDeclNode)) for f in p[1]):
                funcs_list = p[1]
                vars_list = p[2] if p[2] else []
            else:
                vars_list = p[1]
                funcs_list = p[2] if p[2] else []
    elif len(p) == 4:
        vars_list = p[1]
        funcs_list = p[2]
        if p[3] is not None:
            vars_list += p[3]

    # ⚠️ REGISTO AQUI!
    for func in funcs_list:
        if isinstance(func, FunctionDeclNode):
            declared_functions[func.nome] = len(func.parametros)
            declared_variables.add(func.nome)
        elif isinstance(func, ProcedureDeclNode):
            declared_functions[func.name] = len(func.params)

    p[0] = (vars_list, funcs_list)
    print(">>> FUNÇÕES REGISTADAS:", declared_functions)


def p_declaracoes_variaveis_opt(p):
    '''declaracoes_variaveis_opt : declaracoes_variaveis
                                 | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_declaracoes_variaveis(p):
    'declaracoes_variaveis : VAR lista_decl'
    p[0] = p[2]  

def p_lista_decl(p):
    '''lista_decl : lista_decl decl
                  | decl'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_decl(p):
    'decl : lista_ids ":" tipo ";"'
    nomes = []
    for var_node in p[1]:
        nome = var_node.name
        if nome in declared_variables:
            semantic_errors.append(f"Variável '{nome}' já declarada.")
        else:
            declared_variables.add(nome)
        nomes.append(nome)
    p[0] = nomes

def p_tipo(p):
    '''tipo : TIPOVAR
            | TIPOSTRING
            | ARRAY '[' NUMBER DOTDOT NUMBER ']' OF TIPOVAR'''
    p[0] = None

def p_lista_ids(p):
    '''lista_ids : identificador
                 | lista_ids ',' identificador'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_identificador(p):
    '''identificador : ID
                     | ID "[" expressao "]"'''
    if len(p) == 2:
        p[0] = VarNode(p[1])
    else:
        p[0] = IndexNode(VarNode(p[1]), p[3])

def p_declaracoes_subprogramas(p):
    'declaracoes_subprogramas : lista_subprogramas'
    p[0] = p[1]

def p_lista_subprogramas(p):
    '''lista_subprogramas : lista_subprogramas subprograma
                          | subprograma'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_subprograma(p):
    '''subprograma : funcao
                   | procedimento'''
    p[0] = p[1]

def p_funcao_header(p):
    '''funcao_header : FUNCTION ID '(' parametros ')' ':' TIPOVAR ';' '''
    nome_func = p[2]
    parametros = p[4] if p[4] else []

    global declared_variables, declared_functions

    p.parser.old_declared_vars = declared_variables.copy()

    declared_variables = set()

    declared_variables.add(nome_func)

    for param in parametros:
        declared_variables.add(param.name)

    declared_functions[nome_func] = len(parametros)

    p[0] = (nome_func, parametros)

def p_funcao(p):
    '''funcao : funcao_header bloco_simples'''
    nome_func, parametros = p[1]
    corpo = p[2]

    global declared_variables
    declared_variables = p.parser.old_declared_vars  

    p[0] = FunctionDeclNode(nome_func, [VarNode(param.name) for param in parametros], corpo)

def p_procedimento(p):
    'procedimento : PROCEDURE ID "(" parametros ")" ";" declaracoes_variaveis_opt bloco_simples ";"'
    param_ids = [v.name for v in p[4]] if p[4] else []
    if p[2] in declared_functions:
        semantic_errors.append(f"Procedimento '{p[2]}' já declarado.")
    else:
        declared_functions[p[2]] = len(param_ids)
    corpo = p[8]
    p[0] = ProcedureDeclNode(p[2], param_ids, corpo)

def p_atribuicao(p):
    '''atribuicao : ID ASSIGN expressao'''
    varname = p[1]
    expr = p[3]
    print(f"⚠️ Atribuição para {p[1]} (declared: {declared_variables})")
    if varname not in declared_variables:
        p[0] = ErrorNode(f"Identificador '{varname}' não declarado.")
    elif expr is None or isinstance(expr, ErrorNode):
        p[0] = ErrorNode(f"Expressão inválida na atribuição a '{varname}'.")
    else:
        p[0] = AssignNode(VarNode(varname), expr)

def p_parametros(p):
    '''parametros : lista_param
                  | empty'''
    p[0] = p[1] if p[1] else []

def p_lista_param(p):
    '''lista_param : lista_param ";" param
                   | param'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]

def p_param(p):
    'param : lista_ids ":" tipo'
    for id in p[1]:
        declared_variables.add(id.name) 
    p[0] = p[1]

def p_comando(p):
    '''comando : atribuicao
               | comando_if
               | comando_for
               | comando_while
               | comando_composto
               | comando_write
               | comando_read
               | chamada_funcao'''
    p[0] = p[1]

def p_comando_write(p):
    'comando_write : WRITELN "(" lista_exp ")"'
    p[0] = WriteNode(p[3])

def p_comando_read(p):
    'comando_read : READLN "(" lista_ids ")"'
    p[0] = ReadNode(p[3])

def p_comando_if(p):
    '''comando_if : IF expressao THEN comando ELSE comando
                  | IF expressao THEN comando %prec LOWER_THAN_ELSE'''
    if len(p) == 7:
        p[0] = IfNode(p[2], p[4], p[6])
    else:
        p[0] = IfNode(p[2], p[4])

def p_comando_for(p):
    '''comando_for : FOR ID ASSIGN expressao TO expressao DO comando
                   | FOR ID ASSIGN expressao DOWNTO expressao DO comando'''
    if p[5].lower() == 'to':
        p[0] = ForNode(VarNode(p[2]), p[4], p[6], p[8], is_downto=False)
    else:
        p[0] = ForNode(VarNode(p[2]), p[4], p[6], p[8], is_downto=True)

def p_comando_while(p):
    'comando_while : WHILE expressao DO comando'
    p[0] = WhileNode(p[2], p[4])

def p_lista_exp(p):
    '''lista_exp : expressao
                 | lista_exp ',' expressao'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_argumentos(p):
    '''argumentos : lista_exp
                  | empty'''
    if p[1] is None:
        p[0] = []
    else:
        p[0] = p[1]

def p_expressao(p):
    '''expressao : expressao OR expressao1
                 | expressao1'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinaryOpNode(p[2], p[1], p[3])

def p_expressao1(p):
    '''expressao1 : expressao1 AND expressao2
                  | expressao2'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinaryOpNode(p[2], p[1], p[3])

def p_expressao2_index(p):
    '''expressao2 : ID '[' expressao ']' '''
    p[0] = IndexAccessNode(VarNode(p[1]), p[3])

def p_expressao2(p):
    '''expressao2 : expressao3 relop expressao3
                  | expressao3'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinaryOpNode(p[2], p[1], p[3])

def p_relop(p):
    '''relop : EQ
             | NEQ
             | LT
             | LE
             | GT
             | GE'''
    p[0] = p[1]



def p_expressao3(p):
    '''expressao3 : expressao3 addop termo
                  | termo'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinaryOpNode(p[2], p[1], p[3])

def p_addop(p):
    '''addop : '+'
             | '-' '''
    p[0] = p[1]

def p_termo(p):
    '''termo : termo mulop fator
             | fator'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinaryOpNode(p[2], p[1], p[3])

def p_mulop(p):
    '''mulop : '*'
             | '/'
             | DIV
             | MOD'''
    p[0] = p[1]

def p_fator(p):
    '''fator : NUMBER
             | STRING
             | TRUE
             | FALSE
             | ID
             | ID "[" expressao "]"
             | "(" expressao ")"
             | chamada_funcao'''

    if len(p) == 2:
        if p.slice[1].type == 'NUMBER':
            p[0] = NumberNode(p[1])
        elif p.slice[1].type == 'STRING':
            p[0] = StringNode(p[1])
        elif p.slice[1].type == 'TRUE':
            p[0] = BooleanNode(True)
        elif p.slice[1].type == 'FALSE':
            p[0] = BooleanNode(False)
        elif isinstance(p[1], FuncCallNode) or isinstance(p[1], ErrorNode):
            p[0] = p[1]
        else:
            p[0] = VarNode(p[1])
    elif len(p) == 4 and p[2] == '[':
        p[0] = IndexNode(VarNode(p[1]), p[3])
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]

def p_chamada_funcao(p):
    '''chamada_funcao : ID "(" argumentos ")"'''
    func_name = p[1]
    args = p[3]

    total_args = len(args)
    esperado = declared_functions.get(func_name, funcoes_embutidas.get(func_name))

    if esperado is None:
        semantic_errors.append(f"Função ou procedimento '{func_name}' não declarado.")
        p[0] = ErrorNode(f"Função '{func_name}' não declarada.")
    elif total_args != esperado:
        semantic_errors.append(f"'{func_name}' chamado com {total_args} argumentos, mas esperava {esperado}.")
        p[0] = ErrorNode(f"Chamada a '{func_name}' com número errado de argumentos.")
    elif not all(isinstance(arg, ASTNode) for arg in args):
        semantic_errors.append(f"Argumentos inválidos na chamada de '{func_name}'.")
        p[0] = ErrorNode(f"Chamada inválida a '{func_name}'.")
    else:
        p[0] = FuncCallNode(func_name, args)
        print(f">>> Parsing chamada a função: {func_name} com args {args}")


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}: token inesperado '{p.value}'")
        parser.errok()
    else:
        print("Erro de sintaxe no fim do input")

declared_functions.update(funcoes_embutidas)
parser = yacc.yacc(start='programa')