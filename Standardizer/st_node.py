from enum import Enum, auto

class STNodeType(Enum):
    LET = auto()
    WHERE = auto()  
    GAMMA = auto()
    LAMBDA = auto()
    YSTAR = auto()
    TAU = auto()
    AUG = auto()
    COMMA = auto()
    EQ = auto()
    COND = auto()
    TRUE = auto()
    FALSE = auto()
    NIL = auto()
    IDENT = auto()
    INT = auto()
    STR = auto()
    OP = auto()
    ID = auto()

class STNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children
    
    def get_data(self):
        return self.value if self.value else self.node_type.name.lower()

    def print(self, indent=0):
        label = self.value if self.value else self.node_type.name.lower()
        print("." * indent + str(label))
        for child in self.children:
            child.print(indent + 1)
