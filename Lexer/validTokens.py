from enum import Enum

class validTokenTypes(Enum):
    Identifier = 1
    Integer = 2
    Operator = 3
    String = 4
    Punction = 5
    Keyword = 6
    End_of_tokens = 7

class validToken:

    def __init__(self, tokenType, context):
        if(not isinstance(tokenType, validTokenTypes)):
            raise ValueError("Token type isn't valid.")
        else:
            self.tokenType = tokenType
            self.context = context
    
    def getType(self):
        return self.tokenType

    def getContext(self):
        return self.context
        
    