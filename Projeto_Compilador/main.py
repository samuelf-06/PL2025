import sys
from pascal_lex import lexer
from pascal_parser import *
from ast_nodes import *

# === Funções de utilidade ===
def read_input_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def write_output_file(filename, data):
    with open(filename, 'w', encoding='utf-8', newline='\n') as file:
        file.write(data)

# === Análise Léxica ===
def run_lexer(filename):
    print("===== Análise Léxica =====")
    data = read_input_file(filename)
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    print("Fim da análise léxica.\n")

# === Impressão da AST (detalhada) ===
def print_ast(node, indent=0):
    prefix = "  " * indent
    if isinstance(node, list):
        for elem in node:
            print_ast(elem, indent)
    elif isinstance(node, ASTNode):
        print(f"{prefix}{type(node).__name__}")
        for attr, value in vars(node).items():
            if isinstance(value, ASTNode) or isinstance(value, list):
                print(f"{prefix}  {attr}:")
                print_ast(value, indent + 1)
            else:
                print(f"{prefix}  {attr}: {value}")

# === Verificação Semântica ===
def verificar_semantica(ast):
    if isinstance(ast, FuncCallNode):
        if ast.name not in declared_functions:
            semantic_errors.append(f"Função '{ast.name}' chamada mas não foi declarada.")
        else:
            esperado = declared_functions[ast.name]
            real = len(ast.args)
            if real != esperado:
                semantic_errors.append(f"Função '{ast.name}' chamada com {real} argumentos, mas esperava {esperado}.")
    elif isinstance(ast, AssignNode):
        if isinstance(ast.var, ErrorNode):
            semantic_errors.append(f"Identificador inválido na atribuição: {ast.var.message}")
        elif not isinstance(ast.expr, ASTNode):
            semantic_errors.append(f"Expressão inválida na atribuição a '{ast.var.name}'. Esperado nó da AST, obtido {type(ast.expr).__name__}.")
        elif isinstance(ast, IndexAccessNode):
            if not isinstance(ast.array, VarNode):
                semantic_errors.append(f"Acesso a índice inválido: {ast.array}")



    for attr in vars(ast).values():
        if isinstance(attr, list):
            for item in attr:
                if isinstance(item, ASTNode):
                    verificar_semantica(item)
        elif isinstance(attr, ASTNode):
            verificar_semantica(attr)

# === Análise Sintática e Semântica ===
def run_parser(filename):
    print("===== Análise Sintática e Semântica =====")
    data = read_input_file(filename)

    declared_functions.clear()
    declared_variables.clear()
    semantic_errors.clear()

    result_ast = parser.parse(data, tracking=True)

    print("\n===== AST Gerada =====")
    print(result_ast)

    print("===== DEBUG AST =====")
    print_ast(result_ast)

    if result_ast:
        mapear_variaveis(result_ast)
        verificar_semantica(result_ast)

        if semantic_errors:
            print("\nErros semânticos encontrados:")
            for err in semantic_errors:
                print("  -", err)
            print("Código NÃO gerado devido a erros semânticos.")
            return
        else:
            print("Análise semântica sem erros.")

        codigo_vm = result_ast.generate_code()
        write_output_file('output.txt', codigo_vm)
        print("\nCódigo gerado com sucesso em 'output.txt'.")
    else:
        print("Erro: parser não gerou AST.")

    print("Fim da análise sintática.\n")

# === Main ===
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python main.py [lexer|parser] <ficheiro_pascal>")
        sys.exit(1)

    mode = sys.argv[1]
    filename = sys.argv[2]

    if mode == "lexer":
        run_lexer(filename)
    elif mode == "parser":
        run_parser(filename)
    else:
        print("Modo inválido. Usa 'lexer' ou 'parser'.")
