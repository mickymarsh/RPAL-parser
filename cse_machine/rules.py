from .node import *

class CSEMachine:
    def __init__(self, control, stack, environment):
        self.control = control
        self.stack = stack
        self.environment = environment

    def execute(self):
        # Execute the CSEMachine
        current_environment = self.environment[0]
        j = 1
        while self.control:
            current_symbol = self.control.pop()
            

            # rule 01
            if isinstance(current_symbol, Id) or isinstance(current_symbol, Int) or isinstance(current_symbol, Ystar):
                
                self.stack.insert(0, current_environment.lookup(current_symbol))

            #rule 02
            elif isinstance(current_symbol, Lambda):
                
                current_symbol.set_environment(current_environment.get_index())
                self.stack.insert(0, current_symbol)

            elif isinstance(current_symbol, Gamma):
                next_symbol = self.stack.pop(0)

                # rule 04
                if isinstance(next_symbol, Lambda):
                    
                    lambda_expr = next_symbol
                    e = Env(j)
                    j += 1
                    if len(lambda_expr.identifiers) == 1:
                        temp = self.stack.pop(0)
                        e.values[lambda_expr.identifiers[0]] = temp
                    else:
                        tup = self.stack.pop(0)
                        for i, id in enumerate(lambda_expr.identifiers):
                            e.values[id] = tup.symbols[i]
                    for env in self.environment:
                        if env.get_index() == lambda_expr.get_environment():
                            e.set_parent(env)
                    current_environment = e
                    self.control.append(e)
                    self.control.append(lambda_expr.get_delta())

                    """for x in self.control:
                        if isinstance(x, Delta):
                            for y in x.symbols:
                                print(y.get_data())
                        print(x.get_data())"""

                    self.stack.insert(0, e)
                    self.environment.append(e)

                # rule 10
                elif isinstance(next_symbol, Aug):
                    
                    # Handle Tup expression
                    tup = next_symbol
                    i = int(self.stack.pop(0).get_data())
                    self.stack.insert(0, tup.symbols[i - 1])

                # rule 12
                elif isinstance(next_symbol, Ystar):
                   
                    # Handle Ystar expression
                    lambda_expr = self.stack[0]
                    self.stack.pop(0)
                    eta = Neeta()
                    eta.set_index(lambda_expr.get_index())
                    eta.set_environment(lambda_expr.get_environment())
                    eta.set_identifier(lambda_expr.identifiers[0])
                    eta.set_lambda(lambda_expr)
                    self.stack.insert(0, eta)

                # rule 13
                elif isinstance(next_symbol, Neeta):
                    
                    # Handle Eta expression
                    eta = next_symbol
                    lambda_expr = eta.get_lambda()
                    self.control.append(Gamma())
                    self.control.append(Gamma())
                    self.stack.insert(0, eta)
                    self.stack.insert(0, lambda_expr)

                else:
                    # Handle other symbols
                    if next_symbol.get_data() == "Print":
                        pass
                    elif next_symbol.get_data() == "Stem":
                        # implement Stem function
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[0])
                        self.stack.insert(0, s)
                    elif next_symbol.get_data() == "Stern":
                        # implement Stern function
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[1:])
                        self.stack.insert(0, s)
                    elif next_symbol.get_data() == "Conc":
                        # implement Conc function
                        s1 = self.stack.pop(0)
                        s2 = self.stack.pop(0)
                        s1.set_data(s1.get_data() + s2.get_data())
                        self.stack.insert(0, s1)
                    elif next_symbol.get_data() == "Order":
                        # implement Order function
                        tup = self.stack.pop(0)
                        n = Int(str(len(tup.symbols)))
                        self.stack.insert(0, n)
                    elif next_symbol.get_data() == "Isinteger":
                        # implement Isinteger function
                        if isinstance(self.stack[0], Int):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    elif next_symbol.get_data() == "Null":
                        # implement Null function
                        pass
                    elif next_symbol.get_data() == "Itos":
                        # implement Itos function
                        pass
                    elif next_symbol.get_data() == "Isstring":
                        # implement Isstring function
                        if isinstance(self.stack[0], Str):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    elif next_symbol.get_data() == "Istuple":
                        # implement Istuple function
                        if isinstance(self.stack[0], Aug):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    elif next_symbol.get_data() == "Istruthvalue":
                        # implement Istruthvalue function
                        if isinstance(self.stack[0], Bool):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    elif next_symbol.get_data() == "Isfunction":
                        # implement Isfunction function
                        if isinstance(self.stack[0], Lambda):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)

            # rule 05
            elif isinstance(current_symbol, Env):
                
                # Handle e expression
                self.stack.pop(1)
                self.environment[current_symbol.get_index()].set_is_removed(True)
                y = len(self.environment)
                while y > 0:
                    if not self.environment[y - 1].get_is_removed():
                        current_environment = self.environment[y - 1]
                        break
                    else:
                        y -= 1

            # rule 06
            elif isinstance(current_symbol, Rator):
                
                if isinstance(current_symbol, Uop):
                    # Handle Unary operation
                    rator = current_symbol
                    rand = self.stack.pop(0)
                    self.stack.insert(0, self.apply_unary_operation(rator, rand))
                if isinstance(current_symbol, Bop):
                    # Handle Binary operation
                    rator = current_symbol
                    rand1 = self.stack.pop(0)
                    rand2 = self.stack.pop(0)
                    self.stack.insert(0, self.apply_binary_operation(rator, rand1, rand2))
                    

            # rule 08
            elif isinstance(current_symbol, Beta):
                
                if (self.stack[0].get_data() == "true"):
                    self.control.pop(-1)
                else:
                    self.control.pop(-2)
                self.stack.pop(0)

            # rule 09
            elif isinstance(current_symbol, Tau):
                
                # Handle Tau expression
                tau = current_symbol
                tup = Aug()
                for _ in range(tau.get_n()):
                    tup.symbols.append(self.stack.pop(0))
                self.stack.insert(0, tup)
            elif isinstance(current_symbol, Delta):
                # Handle Delta expression
                self.control.extend(current_symbol.symbols)

            
            elif isinstance(current_symbol, Container):
                # Handle B expression
                self.control.extend(current_symbol.symbols)
            else:
                self.stack.insert(0, current_symbol)
            

# ================================================================================================================================================= 

    def print_environment(self):
        # Print the environment symbols
        for symbol in self.environment:
            print(f"e{symbol.get_index()} --> ", end="")
            if symbol.get_index() != 0:
                print(f"e{symbol.get_parent().get_index()}")
            else:
                print()
                
    def covert_string_to_bool(self, data):
        if data == "true":
            return True
        elif data == "false":
            return False

    def apply_unary_operation(self, rator, rand):
        # Apply unary operation
        if rator.get_data() == "neg":
            val = int(rand.get_data())
            return Int(str(-1 * val))
        elif rator.get_data() == "not":
            val = self.covert_string_to_bool(rand.get_data())
            return Bool(str(not val).lower())
        else:
            return "Error"

    def apply_binary_operation(self, rator, rand1, rand2):
        # Apply binary operation
        if rator.get_data() == "plus":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Int(str(val1 + val2))
        elif rator.data == "minus":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 - val2))
        elif rator.get_data() == "*":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Int(str(val1 * val2))
        elif rator.get_data() == "/":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Int(str(int(val1 / val2)))
        elif rator.get_data() == "**":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Int(str(val1 ** val2))
        elif rator.get_data() == "&":
            val1 = self.covert_string_to_bool(rand1.get_data())
            val2 = self.covert_string_to_bool(rand2.get_data())
            return Bool(str(val1 and val2).lower())
        elif rator.get_data() == "or":
            val1 = self.covert_string_to_bool(rand1.get_data())
            val2 = self.covert_string_to_bool(rand2.get_data())
            return Bool(str(val1 or val2).lower())
        elif rator.get_data() == "eq":
            val1 = rand1.get_data()
            val2 = rand2.get_data()
            return Bool(str(val1 == val2).lower())
        elif rator.get_data() == "ne":
            val1 = rand1.get_data()
            val2 = rand2.get_data()
            return Bool(str(val1 != val2).lower())
        elif rator.get_data() == "ls":
            val1 = rand1.get_data()
            val2 = rand2.get_data()
            return Bool(str(val1 < val2).lower())
        elif rator.get_data() == "le":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Bool((val1 <= val2))
        elif rator.get_data() == "gr":
            val1 = rand1.get_data()
            val2 = rand2.get_data()
            return Bool(str(val1 > val2).lower())
        elif rator.get_data() == "ge":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Bool(str(val1 >= val2).lower())
        elif rator.get_data() == "aug":
            if isinstance(rand2, Aug):
                rand1.symbols.extend(rand2.symbols)
            else:
                rand1.symbols.append(rand2)
            return rand1
        else:
            return "Error"

    def get_tuple_value(self, tup):
        # Get the value of a tuple
        temp = "("
        for symbol in tup.symbols:
            if isinstance(symbol, Aug):
                temp += self.get_tuple_value(symbol) + ", "
            else:
                temp += symbol.get_data() + ", "
        temp = temp[:-2] + ")"
        return temp

    def get_answer(self):
        # Get the answer from the CSEMachine
        self.execute()
        if isinstance(self.stack[0], Aug):
            return self.get_tuple_value(self.stack[0])
        return self.stack[0].get_data()
# ================================================================================================================================================= 
    
    def print_stack(self):
        print("Stack: ", end="")
        for symbol in self.stack:
            print(symbol.get_data(), end="")
            if isinstance(symbol, (Lambda, Delta, Env, Neeta)):
                print(symbol.get_index(), end="")
            print(",", end="")
        print()
    
    def print_control(self):
        print("Control: ", end="")
        for symbol in self.control:
            print(symbol.get_data(), end="")
            if isinstance(symbol, (Lambda, Delta, Env, Neeta)):
                print(symbol.get_index(), end="")
            print(",", end="")
        print()

# ================================================================================================================================================= 
            
    def write_stack_to_file(self, file_path): 
        with open(file_path, r'D:\UOM\UOM_Files\S4 - Programming Languages') as file:
            for symbol in self.stack:
                file.write(symbol.get_data())
                if isinstance(symbol, (Lambda, Delta, Env, Neeta)):
                    file.write(str(symbol.get_index()))
                file.write(",")
            file.write("\n")

    def write_control_to_file(self, file_path):
        with open(file_path, r'D:\UOM\UOM_Files\S4 - Programming Languages') as file:
            for symbol in self.control:
                file.write(symbol.get_data())
                if isinstance(symbol, (Lambda, Delta, Env, Neeta)):
                    file.write(str(symbol.get_index()))
                file.write(",")
            file.write("\n")
    
    def clear_file(file_path):
        open(file_path, 'w').close()
    



    