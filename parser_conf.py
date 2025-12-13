# parser_conf.py
import sys
import ply.yacc as yacc
from lexer_conf import tokens, lexer

# окружение констант
env = {}

# -------------- грамматика -----------------

def p_program(p):
    """program : statements"""
    p[0] = env

def p_statements_multi(p):
    """statements : statements statement"""
    # env заполняется в p_statement_const
    pass

def p_statements_single(p):
    """statements : statement"""
    pass

def p_statement_const(p):
    """statement : IDENT IS value"""
    name = p[1]
    value = p[3]
    if name in env:
        print(
            f"Семантическая ошибка: повторное объявление константы '{name}'",
            file=sys.stderr
        )
        raise SyntaxError
    env[name] = value

def p_value_atom(p):
    """value : atom"""
    p[0] = p[1]

def p_value_array(p):
    """value : array"""
    p[0] = p[1]

def p_atom_number(p):
    """atom : NUMBER"""
    p[0] = p[1]

def p_atom_string(p):
    """atom : STRING"""
    p[0] = p[1]

def p_atom_constref(p):
    """atom : QMARK_LBRACK IDENT RBRACK"""
    name = p[2]
    if name not in env:
        print(
            f"Семантическая ошибка: использование несуществующей константы '{name}'",
            file=sys.stderr
        )
        raise SyntaxError
    p[0] = env[name]

def p_array_empty(p):
    """array : LPAREN RPAREN"""
    p[0] = []

def p_array_nonempty(p):
    """array : LPAREN array_elements RPAREN"""
    p[0] = p[2]

def p_array_elements_single(p):
    """array_elements : value"""
    p[0] = [p[1]]

def p_array_elements_many(p):
    """array_elements : array_elements COMMA value"""
    p[1].append(p[3])
    p[0] = p[1]

def p_error(p):
    if p is None:
        print("Синтаксическая ошибка: неожиданное окончание файла", file=sys.stderr)
    else:
        print(
            f"Синтаксическая ошибка: токен '{p.value}' (тип {p.type}) "
            f"в строке {p.lineno}",
            file=sys.stderr
        )
    raise SyntaxError

parser = yacc.yacc(start='program', debug=False, write_tables=False)

# -------------- публичная функция -----------------


def parse_config(text: str) -> dict:
    """Разобрать конфигурацию и вернуть dict с константами."""
    global env
    env = {}
    result = parser.parse(text, lexer=lexer)
    return result
