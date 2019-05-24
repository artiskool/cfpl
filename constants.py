# Constant values
# Copyright 2019 Art Layese <artiskool@gmail.com>

from token import Token


INT_CONST       = 'INT_CONST'
FLOAT_CONST     = 'FLOAT_CONST'
CHAR_CONST      = 'CHAR_CONST'
BOOL_CONST      = 'BOOL_CONST'
STRING_CONST    = 'STRING_CONST'
PLUS            = 'PLUS'
MINUS           = 'MINUS'
MUL             = 'MUL'
DIV             = 'DIV'
MOD             = 'MOD'
LEFT_PAREN      = 'LEFT_PAREN'
RIGHT_PAREN     = 'RIGHT_PAREN'
LEFT_BRACE      = 'LEFT_BRACE'
RIGHT_BRACE     = 'RIGHT_BRACE'

ID              = 'ID'
ASSIGN          = 'ASSIGN'
SEMI            = 'SEMI'
DOT             = 'DOT'
COLON           = 'COLON'
COMMA           = 'COMMA'
AMPERSAND       = 'AMPERSAND'
GREATER_THAN    = 'GREATER_THAN'
LESSER_THAN     = 'LESSER_THAN'
GREATER_EQUAL   = 'GREATER_EQUAL'
LESSER_EQUAL    = 'LESSER_EQUAL'
EQUAL           = 'EQUAL'
NOT_EQUAL       = 'NOT_EQUAL'

EOF = 'EOF'
VAR = 'VAR'
AS = 'AS'
INPUT = 'INPUT'
OUTPUT = 'OUTPUT'
IF = 'IF'
ELSE = 'ELSE'
WHILE = 'WHILE'
START = 'START'
STOP = 'STOP'
INT = 'INT'
BOOL = 'BOOL'
FLOAT = 'FLOAT'
CHAR = 'CHAR'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'

RESERVED_KEYWORDS = {
    'VAR': Token('VAR', 'VAR'),
    'AS': Token('AS', 'AS'),
    'INT': Token('INT', 'INT'),
    'CHAR': Token('CHAR', 'CHAR'),
    'BOOL': Token('BOOL', 'BOOL'),
    'FLOAT': Token('FLOAT', 'FLOAT'),
    'START': Token('START', 'START'),
    'STOP': Token('STOP', 'STOP'),
    'AND': Token('AND', 'AND'),
    'OR': Token('OR', 'OR'),
    'NOT': Token('NOT', 'NOT'),
    'INPUT': Token('INPUT', 'INPUT'),
    'OUTPUT': Token('OUTPUT', 'OUTPUT'),
    'IF': Token('IF', 'IF'),
    'ELSE': Token('ELSE', 'ELSE'),
    'WHILE': Token('WHILE', 'WHILE'),
}
