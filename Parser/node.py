from enum import Enum, auto

class NodeType(Enum):
    let = auto()
    lambda_ = auto()     # 'lambda' is a Python keyword, so we use lambda_
    where = auto()
    tau = auto()
    aug = auto()
    gre = auto()       # for '->' expression
    or_ = auto()         # 'or' is also a Python keyword
    and_ = auto()
    not_ = auto()
    gr = auto()
    ge = auto()
    ls = auto()
    le = auto()
    eq = auto()
    ne = auto()
    plus = auto()
    minus = auto()
    neg = auto()
    mul = auto()
    div = auto()
    pow = auto()         # for '**'
    at = auto()
    gamma = auto()
    true = auto()
    false = auto()
    nil = auto()
    dummy = auto()
    within = auto()
    andop = auto()       # distinguish definition-level 'and'
    rec = auto()
    equal = auto()
    fcn_form = auto()
    identifier = auto()
    integer = auto()
    string = auto()
    comma = auto()
    empty_params = auto()

class ParseNode:
    def __init__(self, node_type, children=None, value=None,tokens=None):
        self.tokens = tokens
        self.node_type = node_type
        self.children = children if children is not None else []
        self.value = value  # Optional, for terminal values like identifier or integer
        self.pos = 0  # Initialize position for token tracking

    def __repr__(self):
        if self.value is not None:
            return f"{self.node_type.name}({self.value})"
        elif self.children:
            return f"{self.node_type.name}({', '.join(map(str, self.children))})"
        else:
            return f"{self.node_type.name}"
    


    def print_tree(self, indent=0):
        print('  ' * indent + str(self))
        if indent == 0 and self.children:
            if isinstance(self.children, list):
                for child in self.children:
                    if child is not None:
                        # print('  ' * (indent + 1) + str(child))
                        break 
                        
                    else:
                        print('  ' * (indent + 1) + "None")
            elif self.children is not None:
                print('  ' * (indent + 1) + str(self.children))
                
            else:
                print('  ' * (indent + 1) + "None")
