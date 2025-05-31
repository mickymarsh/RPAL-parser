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

    # def print(self, indent=0):
    #     if self.value is not None:
    #         if self.node_type == STNodeType.IDENT:
    #             label = f"<ID:{self.value}>"
    #         elif self.node_type == STNodeType.INT:
    #             label = f"<INT:{self.value}>"
    #         elif self.node_type == STNodeType.STR:
    #             label = f"<STR:{self.value}>"
    #         else:
    #             label = self.node_type.name.lower()
    #     else:
    #         label = self.node_type.name.lower()

    #     print("." * indent + str(label))
    #     for child in self.children:
    #         child.print(indent + 1)

    def print(self, indent=0):
        label = self.value if self.value else self.node_type.name.lower()
        print("." * indent + str(label))
        for child in self.children:
            child.print(indent + 1)
