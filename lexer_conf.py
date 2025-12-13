# lexer_conf.py
import sys
import ply.lex as lex

tokens = (
    'NUMBER',
    'STRING',
    'IDENT',
    'IS',
    'QMARK_LBRACK',
    'RBRACK',
    'LPAREN',
    'RPAREN',
    'COMMA',
)

reserved = {
    'is': 'IS',
}

t_QMARK_LBRACK = r'\?\['
t_RBRACK       = r'\]'
t_LPAREN       = r'\('
t_RPAREN       = r'\)'
t_COMMA        = r','

def t_NUMBER(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'@\"[^\"\n]*\"'
    text = t.value
    t.value = text[2:-1]   # @"..." -> ...
    return t

def t_IDENT(t):
    r'[_a-zA-Z]+'
    t.type = reserved.get(t.value, 'IDENT')
    return t

def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    # игнорируем комментарии
    pass

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(
        f"Лексическая ошибка: недопустимый символ '{t.value[0]}' "
        f"в позиции {t.lexpos}",
        file=sys.stderr
    )
    t.lexer.skip(1)

lexer = lex.lex()
