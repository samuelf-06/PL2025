funcoes_embutidas = {
    "length": 1,
    "ord": 1,
    "chr": 1
}

var_positions = {} 
next_var_index = 0
declared_variables = set()


label_counter = 0
def gen_label(prefix="L"):
    global label_counter
    label = f"{prefix}{label_counter}"
    label_counter += 1
    return label

class ASTNode:
    def __str__(self):
        return self.__repr__()

    def generate_code(self):
        return ""

class ProgramNode(ASTNode):
    def __init__(self, name, declaracoes, corpo):
        self.name = name
        self.declaracoes = declaracoes
        self.corpo = corpo
    
    def __repr__(self):
        return f"ProgramNode(nome={self.name}, funcoes={self.declaracoes}, corpo={self.corpo})"

    def generate_code(self):
        global var_positions, next_var_index

        code = "start\n"

        var_positions = {}
        next_var_index = 0
        mapear_variaveis(self.corpo)

        code += self.corpo.generate_code()
        code += "stop\n\n"

        for decl in self.declaracoes:
            if isinstance(decl, FunctionDeclNode):
                code += decl.generate_code()
                code += "\n\n"

            elif isinstance(decl, ProcedureDeclNode):
                code += decl.generate_code()
                code += "\n\n"

        return code


class AssignNode(ASTNode):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def generate_code(self):
        if not isinstance(self.expr, ASTNode):
            raise Exception(f"Expressão inválida na atribuição: esperado nó da AST, obtido {type(self.expr).__name__}.")
        code = self.expr.generate_code()
        if isinstance(self.var, VarNode):
            idx = var_positions.get(self.var.name)
            if idx is None:
                raise Exception(f"Variável '{self.var.name}' não declarada.")
            code += f"storeg {idx}\n"
        return code

class IfNode(ASTNode):
    def __init__(self, cond, then_branch, else_branch=None):
        self.cond = cond
        self.then_branch = then_branch
        self.else_branch = else_branch

    def generate_code(self):
        else_lbl = gen_label("else")
        end_lbl = gen_label("endif")
        code = self.cond.generate_code()
        code += f"jz {else_lbl}\n"
        code += self.then_branch.generate_code()
        code += f"jump {end_lbl}\n"
        code += f"{else_lbl}:\n"
        if self.else_branch:
            code += self.else_branch.generate_code()
        code += f"{end_lbl}:\n"
        return code

class WhileNode(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def generate_code(self):
        start_lbl = gen_label("while")
        end_lbl = gen_label("endw")
        code = f"{start_lbl}:\n"
        code += self.cond.generate_code()
        code += f"jz {end_lbl}\n"
        code += self.body.generate_code()
        code += f"jump {start_lbl}\n"
        code += f"{end_lbl}:\n"
        return code

class BinaryOpNode(ASTNode):
    def __init__(self, op, left, right):
        if not isinstance(left, ASTNode):
            raise Exception(f"[ERRO] Left operand não é ASTNode: {left} ({type(left).__name__})")
        if not isinstance(right, ASTNode):
            raise Exception(f"[ERRO] Right operand não é ASTNode: {right} ({type(right).__name__})")

        self.op = op
        self.left = left
        self.right = right


    def generate_code(self):
        code = self.left.generate_code()
        code += self.right.generate_code()
        ops = {
            '+': 'add',
            '-': 'sub',
            '*': 'mul',
            '/': 'div',
            'div': 'div',
            'mod': 'mod',
            '=': 'equal',
            '<>': ('equal', 'not'),
            '<': 'inf',
            '>': 'sup',
            '<=': 'infeq',
            '>=': 'supeq',
            'and': 'and',
            'or': 'or'
        }
        op_instr = ops.get(self.op, 'nop')
        if isinstance(op_instr, tuple):
            for instr in op_instr:
                code += instr + "\n"
        else:
            code += op_instr + "\n"

        return code

class VarNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def generate_code(self):
        idx = var_positions.get(self.name)
        if idx is None:
            raise Exception(f"Variável '{self.name}' não declarada.")
        return f"pushg {idx}\n"

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def generate_code(self):
        return f"pushi {self.value}\n"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def generate_code(self):
        return f'pushs "{self.value}"\n'

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def generate_code(self):
        return f"pushi {int(self.value)}\n"

class CompoundNode(ASTNode):
    def __init__(self, comandos):
        self.comandos = comandos

    def generate_code(self):
        return ''.join(cmd.generate_code() for cmd in self.comandos)

class WriteNode(ASTNode):
    def __init__(self, valores):
        self.valores = valores

    def generate_code(self):
        code = ""
        for val in self.valores:
            code += val.generate_code()

            if isinstance(val, StringNode):
                code += "writes\n"
            elif isinstance(val, VarNode):
                idx = var_positions.get(val.name)
                if idx is None:
                    raise Exception(f"Variável '{val.name}' não declarada.")
                
                code += f"pushg {idx}\n"
                if val.name.lower().startswith("msg") or val.name.lower().startswith("txt"):
                    code += "writes\n"
                else:
                    code += "writei\n"

            else:
                code += val.generate_code()
                code += "writei\n"



        code += "writeln\n"
        return code

class ReadNode(ASTNode):
    def __init__(self, vars):
        self.vars = vars

    def generate_code(self):
        code = ""
        for v in self.vars:
            code += "read\n"
            code += "atoi\n"  

            if isinstance(v, VarNode):
                idx = var_positions.get(v.name)
                if idx is None:
                    raise Exception(f"Variável '{v.name}' não declarada.")
                code += f"storeg {idx}\n"

            elif isinstance(v, IndexNode):
                code += v.array.generate_code()   
                code += v.index.generate_code()   
                code += "add\n"
                code += "storen\n"               

            else:
                raise Exception(f"Leitura não suportada para {v}")
        return code

class FuncCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args or []

    def __repr__(self):
        return f"FuncCallNode({self.name}, {self.args})"

    def generate_code(self):
        code = "".join(arg.generate_code() for arg in self.args)

        embutidas = {
            "length": "strlen",
            "ord": "ord",
            "chr": "chr",
            "abs": "abs",
            "sqrt": "sqrt",
            "round": "round",
            "trunc": "trunc",
            "upcase": "upcase",
            "lowercase": "lowcase",
            "pos": "pos",
            "copy": "copy",
            "concat": "concat",
            "insert": "insert",
            "delete": "delete",
            "val": "val",
            "str": "str",
        }

        if self.name in embutidas:
            code += embutidas[self.name] + "\n"
        elif self.name == "sqr":
            code += "dup\nmul\n"
        elif self.name == "succ":
            code += "pushi 1\nadd\n"
        elif self.name == "pred":
            code += "pushi 1\nsub\n"
        else:
            code += f"call {self.name}\n"

        return code

class ForNode(ASTNode):
    def __init__(self, var, start, end, body, is_downto=False):
        self.var = var
        self.start = start
        self.end = end
        self.body = body
        self.is_downto = is_downto

    def generate_code(self):
        idx = var_positions.get(self.var.name)
        if idx is None:
            raise Exception(f"Variável '{self.var.name}' não declarada.")

        loop_lbl = gen_label("for")
        end_lbl = gen_label("endfor")
        code = self.start.generate_code()
        code += f"storeg {idx}\n"
        code += f"{loop_lbl}:\n"
        code += f"pushg {idx}\n"
        code += self.end.generate_code()
        cmp_op = "supeq" if self.is_downto else "infeq"
        code += f"{cmp_op}\n"
        code += f"jz {end_lbl}\n"
        code += self.body.generate_code()
        code += f"pushg {idx}\n"
        code += "pushi -1\n" if self.is_downto else "pushi 1\n"
        code += "add\n"
        code += f"storeg {idx}\n"
        code += f"jump {loop_lbl}\n"
        code += f"{end_lbl}:\n"
        return code

class FunctionDeclNode(ASTNode):
    def __init__(self, nome, parametros, corpo):
        self.nome = nome
        self.parametros = parametros or []
        self.corpo = corpo

    def __repr__(self):
        return f"FunctionDeclNode(nome={self.nome}, parametros={self.parametros}, corpo={self.corpo})"

    def generate_code(self):
        global declared_variables, var_positions, next_var_index

        code = f"{self.nome}:\n"
        old_declared = declared_variables.copy()
        old_positions = var_positions.copy()
        old_index = next_var_index
        declared_variables = set()
        var_positions = {}
        next_var_index = 0

        for param in self.parametros:
            declared_variables.add(param.name)
            var_positions[param.name] = next_var_index
            next_var_index += 1

        mapear_variaveis(self.corpo)

        for cmd in self.corpo.comandos:
            code += cmd.generate_code()

        code += "return\n"

        declared_variables = old_declared
        var_positions = old_positions
        next_var_index = old_index

        return code



class ProcedureDeclNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ProcedureDeclNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def generate_code(self):
        global var_positions, next_var_index

        code = f"{self.name}:\n"
        old_positions = var_positions.copy()
        old_index = next_var_index

        for param in self.params:
            if param not in var_positions:
                var_positions[param] = next_var_index
                next_var_index += 1

        code += self.body.generate_code()

        var_positions = old_positions
        next_var_index = old_index

        code += "return\n" 
        return code




class IndexNode:
    def __init__(self, array, index_expr):
        self.array = array 
        self.index = index_expr  

    def generate_code(self):
        code = ''
        print(">> DEBUG IndexNode: self.array =", self.array)
        code += self.array.generate_code()
        code += self.index.generate_code()
        code += 'add\n'
        code += 'loadn\n'
        return code
    
class IndexAccessNode(ASTNode):
    def __init__(self, array, index):
        self.array = array 
        self.index = index  

    def __repr__(self):
        return f"IndexAccessNode(array={self.array}, index={self.index})"

    def generate_code(self):
        code = self.index.generate_code()
        code += self.array.generate_code()
        code += "charat\n"
        return code


class ErrorNode(ASTNode):
    def __init__(self, message):
        self.message = message

    def generate_code(self):
        raise Exception(f"Erro na AST: {self.message}")

def mapear_variaveis(ast):
    global var_positions, next_var_index
    def visitar(node):
        global next_var_index
        if isinstance(node, VarNode):
            if node.name not in var_positions:
                var_positions[node.name] = next_var_index
                next_var_index += 1
        elif hasattr(node, '__dict__'):
            for attr in vars(node).values():
                if isinstance(attr, list):
                    for item in attr:
                        visitar(item)
                elif isinstance(attr, ASTNode):
                    visitar(attr)

    visitar(ast)

