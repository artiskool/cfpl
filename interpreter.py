# Main interpreter file
# Copyright 2019 Art Layese <artiskool@gmail.com>

from parser import *
from lexer import *


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        import collections
        self.GLOBAL_SCOPE = collections.OrderedDict()
        self.DECLARED_VAR = {}

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def assign_var_value(self, name, value):
        if name in self.DECLARED_VAR:
            if self.DECLARED_VAR[name] == INT:
                if not isinstance(value, int):
                    if isinstance(value, float):
                        value = int(value)
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            raise NameError('Value ' + repr(value) + ' could not assign to int variable ' + repr(name))
            elif self.DECLARED_VAR[name] == FLOAT:
                if not isinstance(value, float):
                    if isinstance(value, int):
                        value = float(value)
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            raise NameError('Value ' + repr(value) + ' could not assign to float variable ' + repr(name))
            elif self.DECLARED_VAR[name] == CHAR:
                if not isinstance(value, str):
                    raise NameError('Value ' + repr(value) + ' could not assign to char variable ' + repr(name))
            elif self.DECLARED_VAR[name] == BOOL:
                if value not in ['TRUE', 'FALSE']:
                    if isinstance(value, bool):
                        value = 'TRUE' if value else 'FALSE'
                    else:
                        raise NameError('Value ' + repr(value) + ' could not assign to boolean variable ' + repr(name))
            else:
                raise NameError('Unknown data type ' + self.DECLARED_VAR[name])
            self.GLOBAL_SCOPE[name] = value
        #else: # ignore for now
            #raise NameError(repr(name) + ' variable not defined.')
        return value

    def visit_VarDecl(self, node):
        if node.var_node.value in self.DECLARED_VAR:
            raise NameError(repr(node.var_node.value) + " variable already defined")
        if node.var_node.default_value == None:
            if node.type_node.value == INT:
                default_value = 0
            elif node.type_node.value == FLOAT:
                default_value = 0
            elif node.type_node.value == CHAR:
                default_value = ''
            elif node.type_node.value == BOOL:
                default_value = 'FALSE'
            else:
                default_value = node.var_node.default_value
        else:
            default_value = node.var_node.default_value.value
        self.DECLARED_VAR[node.var_node.value] = node.type_node.value
        self.assign_var_value(node.var_node.value, default_value)

    def visit_Type(self, node):
        # Do nothing
        pass

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == MOD:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == ASSIGN:
            # LIMITATIONS: for multiple assignments, constant values must be enclosed in braces
            value = self.visit(node.right)
            if node.value is None:
                node.value = value
            # process all lefts
            if type(node.left).__name__ == 'BinOp':
                node.left.value = node.value
                return self.visit(node.left)
            if type(node.left).__name__ == 'Var' and node.left.value in self.GLOBAL_SCOPE:
                self.assign_var_value(node.left.value, node.value)
            if type(node.right).__name__ == 'Var' and node.right.value in self.GLOBAL_SCOPE:
                self.assign_var_value(node.right.value, node.value)
            return value
        elif node.op.type == AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == OR:
            return self.visit(node.left) or self.visit(node.right)
        elif node.op.type == NOT:
            return not self.visit(node.right)
        elif node.op.type == GREATER_THAN:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == LESSER_THAN:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == GREATER_EQUAL:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == LESSER_EQUAL:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == EQUAL:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == NOT_EQUAL:
            return bool(self.visit(node.left) != self.visit(node.right))

    def visit_Num(self, node):
        return node.value

    def visit_Char(self, node):
        return node.value

    def visit_Bool(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Input(self, node):
        output = ''
        data_types = []
        for val in node.value:
            data_types.append(self.DECLARED_VAR[val.value])

        inputs = raw_input('please input ' + str(len(node.value)) + ' values separated by comma [' + ', '.join(data_types) + '] >>> ')
        print(inputs)
        values = inputs.split(',')
        if len(values) != len(node.value):
            raise NameError("Invalid inputs.")
        i = 0
        for val in node.value:
            value = values[i]
            data_type = self.DECLARED_VAR[val.value]
            if data_type == INT:
                try:
                    value = int(value)
                except ValueError:
                    raise NameError('Invalid input ' + repr(value) + ' for int variable ' + repr(val.value))
            elif data_type == FLOAT:
                try:
                    value = int(value)
                except ValueError:
                    raise NameError('Invalid input ' + repr(value) + ' for int variable ' + repr(val.value))
            elif data_type == CHAR:
                value = value[0] if len(value) > 0 else value
            elif data_type == BOOL:
                if type(value) is bool:
                    value = 'TRUE' if value else 'FALSE'
                value = str(value)
                if value not in ['TRUE', 'FALSE']:
                    value = 'FALSE'
            else:
                value = str(value)
            self.assign_var_value(val.value, value)
            i = i + 1
        return node.value

    def visit_Output(self, node):
        output = ''
        for val in node.value:
            if type(val).__name__ == 'Var':
                if val.value not in self.GLOBAL_SCOPE:
                    raise NameError(repr(val.value) + " variable is not defined.")
                val_name = val.value
                val = self.GLOBAL_SCOPE[val_name]
                data_type = self.DECLARED_VAR[val_name]
                if data_type == INT:
                    val = int(val)
                elif data_type == FLOAT:
                    val = float(val)
                elif data_type == CHAR:
                    val = val[0] if len(val) > 0 else val
                elif data_type == BOOL:
                    if type(val) is bool:
                        val = 'TRUE' if val else 'FALSE'
                    val = str(val)
                    if val not in ['TRUE', 'FALSE']:
                        val = 'FALSE'
                else:
                    val = str(val)
            else:
                val = val.value
            output += str(val)
        print(output)
        return node.value

    def visit_IfStatement(self, node):
        val_expr = self.visit(node.expr)
        if val_expr and val_expr != 'FALSE':
            values = [node.value]
            if type(node.value).__name__ == 'list':
                values = []
                for val in node.value:
                    values.append(val)
            for val in values:
                self.visit(val)
        elif node.els is not None:
            self.visit(node.els)
        return node.value

    def visit_WhileStatement(self, node):
        while True:
            val_expr = self.visit(node.expr)
            if not val_expr or val_expr == 'FALSE':
                break
            values = [node.value]
            if type(node.value).__name__ == 'list':
                values = []
                for val in node.value:
                    values.append(val)
            for val in values:
                self.visit(val)
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            if child is not None:
                self.visit(child)

    def visit_Assign(self, node):
        values = [node.left]
        if type(node.left.value).__name__ == 'list':
            values = []
            for val in node.left.value:
                values.append(val)
        for val in values:
            var_name = val.value
            if val.token.type != STRING_CONST and var_name not in self.DECLARED_VAR:
                raise NameError(repr(var_name) + " variable is not defined.")
            self.assign_var_value(var_name, self.visit(node.right))
        return
        ### codes below may also work
        value = node.left.value
        if type(value).__name__ == 'list':
            node.left.value = ''
            for val in value:
                node.left.value += val.value
        var_name = node.left.value
        if var_name not in self.DECLARED_VAR:
            raise NameError(repr(var_name) + " variable is not defined")
        self.assign_var_value(var_name, self.visit(node.right))

    def visit_Var(self, node):
        var_name = node.value
        var_value = self.GLOBAL_SCOPE.get(var_name)
        if var_value is None:
            raise NameError(repr(var_name))
        else:
            return var_value

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)



def main():
    import sys
    text = open(sys.argv[1], 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    try:
        result = interpreter.interpret()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
