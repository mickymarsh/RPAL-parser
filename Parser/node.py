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
    


    def print_tree_as_string(self, indent=0):
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

    def print_tree(self, indent=0):
        # Format the current node
        if self.value is not None:
            if self.node_type == NodeType.identifier:
                formatted_value = f"<ID:{self.value}>"
            elif self.node_type == NodeType.integer:
                formatted_value = f"<INT:{self.value}>"
            elif self.node_type == NodeType.string:
                formatted_value = f"<STR:{self.value}>"
            else:
                formatted_value = f"{self.node_type.name}({self.value})"
        else:
            # Map node types to desired format
            if self.node_type == NodeType.fcn_form:
                formatted_value = "function_form"
            elif self.node_type == NodeType.gre:
                formatted_value = "->"
            elif self.node_type == NodeType.gr:
                formatted_value = "gr"
            elif self.node_type == NodeType.neg:
                formatted_value = "-"
            elif self.node_type == NodeType.plus:
                formatted_value = "+"
            elif self.node_type == NodeType.minus:
                formatted_value = "-"
            elif self.node_type == NodeType.mul:
                formatted_value = "*"
            elif self.node_type == NodeType.div:
                formatted_value = "/"
            elif self.node_type == NodeType.pow:
                formatted_value = "**"
            elif self.node_type == NodeType.eq:
                formatted_value = "eq"
            elif self.node_type == NodeType.equal:
                formatted_value = "="
            elif self.node_type == NodeType.comma:
                formatted_value = ","
            elif self.node_type == NodeType.andop:
                formatted_value = "and"
            elif self.node_type == NodeType.or_:
                formatted_value = "or"
            elif self.node_type == NodeType.and_:
                formatted_value = "&"
            elif self.node_type == NodeType.not_:
                formatted_value = "not"
            elif self.node_type == NodeType.ge:
                formatted_value = "ge"
            elif self.node_type == NodeType.le:
                formatted_value = "le"
            elif self.node_type == NodeType.ls:
                formatted_value = "ls"
            elif self.node_type == NodeType.ne:
                formatted_value = "!="
            elif self.node_type == NodeType.at:
                formatted_value = "@"
            elif self.node_type == NodeType.within:
                formatted_value = "within"
            elif self.node_type == NodeType.empty_params:
                formatted_value = "()"
            else:
                formatted_value = self.node_type.name
        
        # Print current node with dot indentation
        print('.' * indent + formatted_value)
        
        # Recursively print all children
        if self.children:
            for child in self.children:
                if child is not None:
                    child.print_tree(indent + 1)
