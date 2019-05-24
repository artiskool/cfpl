# Code parser
# Copyright 2019 Art Layese <artiskool@gmail.com>

from constants import *
from ast import *

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        line = str(self.lexer.line + 1)
        if self.current_token.type == EOF:
            line = str(self.lexer.line - 1)
            #line = str(self.lexer.line)
        msg = 'Invalid syntax on line ' + line + ': ' + self.lexer.text
        raise Exception(msg)

    def keep(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "keep" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def block(self):
        """block : declarations compound_statement"""
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):
        """declarations : VAR (variable_declaration)+
                        | empty
        """
        declarations = []
        """
        if self.current_token.type == VAR:
            self.keep(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.keep(SEMI)
        """

        while self.current_token.type == VAR:
            self.keep(VAR)
            if self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)

        return declarations

    def variable_declaration(self):
        """variable_declaration : ID (COMMA ID [= default value])* AS type_spec"""
        node = Var(self.current_token)
        var_nodes = [node]  # first ID
        self.keep(ID)

        if self.current_token.type == ASSIGN:
            self.keep(ASSIGN)
            node.default_value = self.expr()

        while self.current_token.type == COMMA:
            self.keep(COMMA)
            node = Var(self.current_token)
            var_nodes.append(node)
            self.keep(ID)

            if self.current_token.type == ASSIGN:
                self.keep(ASSIGN)
                node.default_value = self.expr()

        self.keep(AS)

        type_node = self.type_spec()
        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations

    def type_spec(self):
        """type_spec : INT
                     | FLOAT
                     | CHAR
                     | BOOL
        """
        token = self.current_token
        if self.current_token.type == INT:
            self.keep(INT)
        elif self.current_token.type == CHAR:
            self.keep(CHAR)
        elif self.current_token.type == BOOL:
            self.keep(BOOL)
        else:
            self.keep(FLOAT)
        node = Type(token)
        return node

    def compound_statement(self):
        """
        compound_statement: START statement_list STOP
        """
        self.keep(START)
        nodes = self.statement_list()
        self.keep(STOP)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement
                       | statement statement_list
        """
        node = self.statement()

        results = [node]
        while self.current_token.type != STOP:
            #self.keep(self.current_token.type) # YAHOOO this is the culprit
            if self.current_token.type == EOF:
                break
            statement = self.statement()
            results.append(statement)
            if type(statement).__name__ == 'NoOp':
                break
        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type == START:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == OUTPUT:
            self.keep(OUTPUT)
            self.keep(COLON)
            self.current_token.value = self.output_statement()
            node = Output(self.current_token)
        elif self.current_token.type == INPUT:
            self.keep(INPUT)
            self.keep(COLON)
            self.current_token.value = self.input_statement()
            node = Input(self.current_token)
        elif self.current_token.type == IF:
            current_token = self.current_token
            self.keep(IF)
            self.keep(LEFT_PAREN)
            expression = self.expr()
            self.keep(RIGHT_PAREN)
            current_token.value = self.compound_statement()
            els = None
            if self.current_token.type == ELSE:
                self.keep(ELSE)
                els = self.compound_statement()
            node = IfStatement(current_token, expression, els)
        elif self.current_token.type == WHILE:
            current_token = self.current_token
            self.keep(WHILE)
            self.keep(LEFT_PAREN)
            expression = self.expr()
            self.keep(RIGHT_PAREN)
            current_token.value = self.compound_statement()
            node = WhileStatement(current_token, expression)
        else:
            node = self.empty()
        return node

    def input_statement(self):
        """
        input_statement: INPUT: (variable)*
        """
        node = Var(self.current_token)
        var_nodes = [node]  # first ID
        self.keep(ID)
        while self.current_token.type == COMMA:
            self.keep(COMMA)
            node = Var(self.current_token)
            var_nodes.append(node)
            self.keep(ID)
            if self.current_token.type == STOP or self.current_token.type == EOF:
                break

        return var_nodes

    def output_statement(self):
        """
        output_statement : expr (& expr)*
        """
        terms = []
        current_pos = self.lexer.pos
        while True:
            if self.current_token.type == STRING_CONST:
                terms.append(self.expr())
            elif self.current_token.type == ID:
                terms.append(self.variable())
            if self.lexer.pos < current_pos or self.current_token.type != AMPERSAND:
                break
            if self.current_token.type == AMPERSAND:
                self.keep(AMPERSAND)
        return terms

    def if_statement(self):
        """
        output_statement : expr (& expr)*
        """
        terms = []
        current_pos = self.lexer.pos
        while True:
            if self.current_token.type == STRING_CONST:
                terms.append(self.expr())
            elif self.current_token.type == ID:
                terms.append(self.variable())
            if self.lexer.pos < current_pos or self.current_token.type != AMPERSAND:
                break
            if self.current_token.type == AMPERSAND:
                self.keep(AMPERSAND)
        return terms

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """

        left = self.variable()
        token = self.current_token
        self.keep(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.keep(ID)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def expr(self):
        """
        expr : term ((PLUS | MINUS | ASSIGN | GREATER_THAN | LESSER_THAN | GREATER_EQUAL | LESSER_EQUAL | EQUAL | NOT_EQUAL) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS, ASSIGN, GREATER_THAN, LESSER_THAN, GREATER_EQUAL, LESSER_EQUAL, EQUAL, NOT_EQUAL):
            token = self.current_token
            if token.type == PLUS:
                self.keep(PLUS)
            elif token.type == MINUS:
                self.keep(MINUS)
            elif token.type == ASSIGN:
                self.keep(ASSIGN)
            elif token.type == GREATER_THAN:
                self.keep(GREATER_THAN)
            elif token.type == LESSER_THAN:
                self.keep(LESSER_THAN)
            elif token.type == GREATER_EQUAL:
                self.keep(GREATER_EQUAL)
            elif token.type == LESSER_EQUAL:
                self.keep(LESSER_EQUAL)
            elif token.type == EQUAL:
                self.keep(EQUAL)
            elif token.type == NOT_EQUAL:
                self.keep(NOT_EQUAL)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """term : factor ((MUL | MOD | DIV | AND | OR | NOT) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, MOD, DIV, AND, OR, NOT):
            token = self.current_token
            if token.type == MUL:
                self.keep(MUL)
            elif token.type == MOD:
                self.keep(MOD)
            elif token.type == DIV:
                self.keep(DIV)
            elif token.type == AND:
                self.keep(AND)
            elif token.type == OR:
                self.keep(OR)
            elif token.type == NOT:
                self.keep(NOT)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """factor : PLUS factor
                  | MINUS factor
                  | INT_CONST
                  | FLOAT_CONST
                  | LEFT_PAREN expr RIGHT_PAREN
                  | SINGLE_QOUTE expr SINGLE_QOUTE
                  | DOUBLE_QOUTE expr DOUBLE_QOUTE
                  | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.keep(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.keep(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INT_CONST:
            self.keep(INT_CONST)
            return Num(token)
        elif token.type == FLOAT_CONST:
            self.keep(FLOAT_CONST)
            return Num(token)
        elif token.type == LEFT_PAREN:
            self.keep(LEFT_PAREN)
            node = self.expr()
            self.keep(RIGHT_PAREN)
            return node
        elif token.type == CHAR_CONST:
            self.keep(CHAR_CONST)
            return Char(token)
        elif token.type == STRING_CONST:
            self.keep(STRING_CONST)
            return String(token)
        elif token.type == BOOL_CONST:
            self.keep(BOOL_CONST)
            return Bool(token)
        else:
            return self.variable()

    def parse(self):
        """
        block : declarations compound_statement

        declarations : VAR (variable_declaration)+
                     | empty

        variable_declaration : ID (COMMA ID [= default value])* AS type_spec

        type_spec : INT | CHAR | FLOAT | BOOL

        compound_statement : START statement_list STOP

        statement_list : statement
                       | statement statement_list

        statement : compound_statement
                  | assignment_statement
                  | empty

        assignment_statement : variable ASSIGN expr

        empty :

        expr : term ((PLUS | MINUS | ASSIGN | GREATER_THAN | LESSER_THAN | GREATER_EQUAL | LESSER_EQUAL | EQUAL | NOT_EQUAL) term)*

        term : factor ((MUL | MOD | DIV | AND | OR | NOT) factor)*

        factor : PLUS factor
               | MINUS factor
               | INT_CONST
               | FLOAT_CONST
               | LEFT_PAREN expr RIGHT_PAREN
               | variable

        variable: ID
        """

        block_node = self.block()
        node = Program(block_node)

        if self.current_token.type != EOF:
            self.error()

        return node

