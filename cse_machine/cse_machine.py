from .node import *
from .rules import CSEMachine
from Standardizer.st_node import *


class CSEMachineFactory:
    def __init__(self):
        self.e0 = Env(0)
        self.i = 1
        self.j = 0

    def get_symbol(self, node: STNode):
        data = node.get_data()
        if data in ("not", "neg"):
            return Uop(data)  # Unary operator symbol
        elif data in ("plus", "minus", "mul", "div", "pow", "and", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"):
            return Bop(data)  # Binary operator symbol
        elif data == "gamma":
            return Gamma()  # Gamma symbol
        elif data == "tau":
            return Tau(len
            (node.get_children()))  # Tau symbol with the number of children
        elif data == "ystar":
            return Ystar()  # Y* symbol
        else:
            if data.startswith("<ID:"):
                return Id(data[4:-1])  # Identifier symbol
            elif data.startswith("<INT:"):
                return Int(data[5:-1])  # Integer symbol
            elif data.startswith("<STR:"):
                return Str(data[6:-2])  # String symbol
            elif data.startswith("<NIL"):
                return Aug()  # Tuple symbol
            elif data.startswith("<TRUE_VALUE:t"):
                return Bool("true")  # Boolean true symbol
            elif data.startswith("<TRUE_VALUE:f"):
                return Bool("false")  # Boolean false symbol
            elif data.startswith("<dummy>"):
                return Dummy()  # Dummy symbol
            else:
                print("Err node:", data)


    def get_b(self, node):
        ae = Container()
        ae.symbols = self.get_pre_order_traverse(node)
        return ae

    def get_lambda(self, node:STNode):
        lambda_expr = Lambda(self.i)
        self.i += 1
        lambda_expr.set_delta(self.get_delta(node.get_children()[1]))
        if node.get_children()[0].get_data() == "comma":
            for identifier in node.get_children()[0].get_children():
                lambda_expr.identifiers.append(Id(identifier.get_data()[4:-1]))
        else:
            lambda_expr.identifiers.append(Id(node.get_children()[0].get_data()[4:-1]))
        return lambda_expr

    def get_pre_order_traverse(self, node: STNode):
        symbols = []
        if node.get_data() == "lambda":
            symbols.append(self.get_lambda(node))  # Lambda expression symbol
        elif node.get_data() == "cond":
            symbols.append(self.get_delta(node.get_children()[1]))  # Delta symbol
            symbols.append(self.get_delta(node.get_children()[2]))  # Delta symbol
            symbols.append(Beta())  # Beta symbol
            symbols.append(self.get_b(node.get_children()[0]))  # B symbol
        else:
            symbols.append(self.get_symbol(node))
            for child in node.get_children():
                symbols.extend(self.get_pre_order_traverse(child))
        return symbols

    def get_delta(self, node):
        delta = Delta(self.j)
        self.j += 1
        delta.symbols = self.get_pre_order_traverse(node)



        # print(delta.index,"th delta is:")  debugging step
        # for x in delta.symbols:
            # print(x.data)

        return delta

    def get_control(self, st):
        #control = [self.e0, self.get_delta(st.get_root())]
        control = [self.e0, self.get_delta(st)]
        return control

    def get_stack(self):
        return [self.e0]

    def get_environment(self):
        return [self.e0]

    def get_cse_machine(self, st):
        control = self.get_control(st)
        stack = self.get_stack()
        environment = self.get_environment()
        return CSEMachine(control, stack, environment)