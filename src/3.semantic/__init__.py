from symbol_table import *
from parse import *

class Semantic:
    def __init__(self, parser, symbolTable):
        self.ast = parser.program()
        self.symbolTable = symbolTable
        self.identifier_variable = {}
        self.identifier_function = {}

    def traverse(self, t):
        #################################
        #   check function is declared?
        #       callTree kid:
        #           *idTree
        #################################
        if isinstance(t, callTree):
            identifier_key = t.getKid(1).getKey()
            identifier_name, identifier_type = self.symbolTable.get_declaration_data(identifier_key)
            if identifier_type is None:
                raise Exception("Error: Function not found '%s'" % identifier_name)

            for tree in t.getKids():
                self.traverse(tree)
        #################################
        #   check function is declared twice?
        #       declrTree kid:
        #           *typeTree
        #           *idTree
        #           *funcHead
        #           *block
        #################################
        elif isinstance(t, funcDeclTree):
            identifier_key = t.getKid(2).getKey()
            identifier_name, identifier_type = self.symbolTable.get_declaration_data(identifier_key)
            if identifier_name in self.identifier_function:
                raise Exception("Error: Function '%s' is declared twice." % identifier_name)
            else:
                self.identifier_function.add(identifier_name)

            for tree in t.getKids():
                self.traverse(tree)
        #################################
        #   check variable is declared?
        #   check variable is declared twice?
        #       declrTree kid:
        #           *typeTree
        #           *idTree
        #################################
        elif isinstance(t, declrTree):
            identifier_key = t.getKid(2).getKey()
            identifier_name, identifier_type = self.symbolTable.get_declaration_data(identifier_key)
            if identifier_type is None:
                raise Exception("Error: Variable not found '%s'" % identifier_name)
            else:
                if identifier_name in self.identifier_variable:
                    raise Exception("Error: Variable '%s' is declared twice." % identifier_name)
                else:
                    self.identifier_variable.add(identifier_name)

            for tree in t.getKids():
                self.traverse(tree)
        # check if function receive enough parameters
        elif isinstance(t, funcHeadTree):
            num_of_function_variables = len(t.getKids())
            if num_of_function_variables is 0:
                return "void"
            else:
                for tree in t.getKids():
        #################################
        #   check if assign has type mismatched.
        #       assignTree kid:
        #           *idTree
        #           assign_op
        #           *expr
        #################################
        elif isinstance(t, assignTree):
        #################################
        #   check if relation has type mismatched.
        #       relOPTree kid:
        #           *expr
        #           rel_op
        #           *expr
        #################################
        elif isinstance(t, relOPTree):
            identifier_type_left = self.traverse(t.getKid(1))
            identifier_type_right = self.traverse(t.getKid(2))
            if identifier_type_left != identifier_type_right:
                raise Exception("Type mismatched between '%s' and '%s'" % (identifier_type_left, identifier_type_right))
            else:
                return 'boolean'
        #################################
        #   check if addOPTree has type mismatched.
        #       addOPTree kid:
        #           *expr
        #           add_op
        #           *expr
        #################################
        elif isinstance(t, addOPTree):
            identifier_type_left = self.traverse(t.getKid(1))
            identifier_type_right = self.traverse(t.getKid(2))

            if identifier_type_left == 'double' and (identifier_type_right in ['double', 'float', 'long', 'int']):
                return identifier_type_left
            elif identifier_type_left == 'String' and identifier_type_right == 'char':
                return identifier_type_left
            elif identifier_type_left == 'int' and identifier_type_right == 'char':
                return identifier_type_left
            else:
                raise Exception("Type mismatched between '%s' and '%s'" % (identifier_type_left, identifier_type_right))
        #################################
        #################################
        #################################
        #################################
        elif isinstance(t, numberTree):
            identifier_type = "int"
            return identifier_type
        elif isinstance(t, stringTree):
            identifier_type = "string"
            return identifier_type











