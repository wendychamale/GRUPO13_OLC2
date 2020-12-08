# -----------------------------------------------------------------------------
# Rainman Sián
# 26-02-2020
#
# Ejemplo interprete sencillo con Python utilizando ply en Ubuntu
# -----------------------------------------------------------------------------

reservadas = {
    'show':'show',
    'databases':'databases',
    'like':'like',
    'select':'select',
    'distinct':'distinct',
    'from':'r_from',
    'alter':'alter',
    ' rename':'rename',
    'to':'to',
    'owner':'owner',
    'table':'table',
    'add':'add',
    'column':'column',
    'set':'set',
    'not':'not',
    'null':'null',
    'check':'check',
    'constraint':'constraint',
    'unique':'unique',
    'foreign':'foreign',
    'key':'key',
    'or':'or',
    'replace':'replace',
    'if':'if',
    'exist':'exist',
    'mode':'mode',
    'inherits':'inherits',
    'primary':'primary',
    'references':'references',
    'default':'default',
    'type':'type',
    'enum':'enum',
    'drop':'drop',
    'update':'update',
    'where':'where',
    'smallint': 'r_smallint',
    'integer': 'r_integer',
    'bigint': 'r_bigint',
    'decimal': 'r_decimal',
    'numeric': 'r_numeric',
    'real': 'r_real',
    'double': 'double',
    'precision': 'precision',
    'money': 'money',
    'character': 'character',
    'varyng': 'varyng',
    'char': 'r_char',
    'timestamp': 'r_timestamp',
    'without': 'without',
    'time': 'time',
    'zone': 'zone',
    'date': 'r_date',
    'time': 'r_time',
    'interval':'interval',
    'boolean':'boolean',
    'true':'true',
    'false':'false',
    'year':'year',
    'month':'month',
    'day':'day',
    'hour':'hour',
    'minute':'minute',
    'second':'second',
    'in':'in',
    'like':'like',
    'ilike':'ilike',
    'similar':'similar',
    'and':'and',
    'or':'or',
    'between':'between',
    'symetric':'symetric',
    'isnull':'isnull',
    'notnull':'notnull',
    'unknown':'unknown',
    'insert':'insert',
    'into':'into'
}

tokens = [
            'mas'
            'menos'
            'elevado'
            'multiplicacion'
            'division'
            'modulo'
            'similar'
            'menor'
            'mayor'
            'igual'
            'menor_igual'
            'mayor_igual'
            'diferente1'
            'diferente2'
            'and'
            'or'
            'ptcoma'
            'llavea'
            'llavec'
            'para'
            'parac'
            'dospuntos'
            'coma'
            'punto'
            'int'
            'decimal'
            'varchar'
            'char'
            'id'
         ] + list(reservadas.values())

# Tokenst_mas = r'\+'
t_menos = r'-'
t_elevado= r'^'
t_multiplicacion = r'\*'
t_division =r'/'
t_modulo= r'%'
t_menor =r'<'
t_mayor =r'>'
t_igual =r'='
t_menor_igual =r'<='
t_mayor_igual =r'>='
t_diferente1=r'<>'
t_diferente2=r'!='
t_simboloor=r'\|'
t_llavea = r'{'
t_llavec = r'}'
t_para = r'\('
t_parc = r'\)'
t_ptcoma =r';'
t_dospuntos=r':'
t_coma=r','
t_punto=r'.'



def t_decimal(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error no se puede convertir %d", t.value)
        t.value = 0
    return t


def t_int(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor numerico incorrecto %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'id')  
    return t


def t_varchar(t):
    r'\'.*?\''
    t.value = t.value[1:-1]  # remuevo las comillas
    return t


# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1


# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Construyendo el analizador léxico
import ply.lex as lex

lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left', 'CONCAT'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('right', 'UMENOS'),
)

# Definición de la gramática

from expresiones import *
from instrucciones import *


def p_init(t):
    'init            : instrucciones'
    t[0] = t[1]


def p_instrucciones_lista(t):
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t):
    'instrucciones    : instruccion '
    t[0] = [t[1]]


def p_instruccion(t):
    '''instruccion      : imprimir_instr
                        | definicion_instr
                        | asignacion_instr
                        | mientras_instr
                        | if_instr
                        | if_else_instr'''
    t[0] = t[1]


def p_instruccion_imprimir(t):
    'imprimir_instr     : IMPRIMIR PARIZQ expresion_cadena PARDER PTCOMA'
    t[0] = Imprimir(t[3])


def p_instruccion_definicion(t):
    'definicion_instr   : NUMERO ID PTCOMA'
    t[0] = Definicion(t[2])


def p_asignacion_instr(t):
    'asignacion_instr   : ID IGUAL expresion_numerica PTCOMA'
    t[0] = Asignacion(t[1], t[3])


def p_mientras_instr(t):
    'mientras_instr     : MIENTRAS PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] = Mientras(t[3], t[6])


def p_if_instr(t):
    'if_instr           : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] = If(t[3], t[6])


def p_if_else_instr(t):
    'if_else_instr      : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER ELSE LLAVIZQ instrucciones LLAVDER'
    t[0] = IfElse(t[3], t[6], t[10])


def p_expresion_binaria(t):
    '''expresion_numerica : expresion_numerica MAS expresion_numerica
                        | expresion_numerica MENOS expresion_numerica
                        | expresion_numerica POR expresion_numerica
                        | expresion_numerica DIVIDIDO expresion_numerica'''
    if t[2] == '+':
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)
    elif t[2] == '-':
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS)
    elif t[2] == '*':
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR)
    elif t[2] == '/':
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)


def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion_numerica %prec UMENOS'
    t[0] = ExpresionNegativo(t[2])


def p_expresion_agrupacion(t):
    'expresion_numerica : PARIZQ expresion_numerica PARDER'
    t[0] = t[2]


def p_expresion_number(t):
    '''expresion_numerica : ENTERO
                        | DECIMAL'''
    t[0] = ExpresionNumero(t[1])


def p_expresion_id(t):
    'expresion_numerica   : ID'
    t[0] = ExpresionIdentificador(t[1])


def p_expresion_concatenacion(t):
    'expresion_cadena     : expresion_cadena CONCAT expresion_cadena'
    t[0] = ExpresionConcatenar(t[1], t[3])


def p_expresion_cadena(t):
    'expresion_cadena     : CADENA'
    t[0] = ExpresionDobleComilla(t[1])


def p_expresion_cadena_numerico(t):
    'expresion_cadena     : expresion_numerica'
    t[0] = ExpresionCadenaNumerico(t[1])


def p_expresion_logica(t):
    '''expresion_logica : expresion_numerica MAYQUE expresion_numerica
                        | expresion_numerica MENQUE expresion_numerica
                        | expresion_numerica IGUALQUE expresion_numerica
                        | expresion_numerica NIGUALQUE expresion_numerica'''
    if t[2] == '>':
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE)
    elif t[2] == '<':
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MENOR_QUE)
    elif t[2] == '==':
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.IGUAL)
    elif t[2] == '!=':
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.DIFERENTE)


def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc

parser = yacc.yacc()


def parse(input):
    return parser.parse(input)