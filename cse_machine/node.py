# AE 
class Delta:
    def __init__(self, i):
        self.data = "delta"
        self.index = i
        self.symbols = []

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index
    
# ----------------------------------------------------------------------------------------------------------------------------------------------
# environment

class Env:
    def __init__(self, i):
        self.data = "e"
        self.index = i
        self.parent = None
        self.is_removed = False
        self.values = {}

    def set_parent(self, e):
        self.parent = e

    def get_parent(self):
        return self.parent

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index

    def set_is_removed(self, is_removed):
        self.is_removed = is_removed

    def get_is_removed(self):
        return self.is_removed

    def lookup(self, id):
        for key in self.values:
            if key.get_data() == id.get_data():
                return self.values[key]
        if self.parent is not None:
            return self.parent.lookup(id)
        else:
            return Id(id.get_data())

# --------------------------------------------------------------------------------------------------------------------------------------------

class Gamma:
    def __init__(self):
        self.data = "gamma"

class Lambda:
    def __init__(self, i):
        self.data = "lambda"
        self.index = i
        self.environment = None
        self.identifiers = []
        self.delta = None

    def set_environment(self, n):
        self.environment = n

    def get_environment(self):
        return self.environment

    def set_delta(self, delta):
        self.delta = delta

    def get_delta(self):
        return self.delta
    def get_index(self):
        return self.index
    
class Neeta:
    def __init__(self):
        self.data = "neeta"
        self.index = None
        self.environment = None
        self.identifier = None
        self.lambda_ = None

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index

    def set_environment(self, e):
        self.environment = e

    def get_environment(self):
        return self.environment

    def set_identifier(self, identifier):
        self.identifier = identifier

    def set_lambda(self, lambda_):
        self.lambda_ = lambda_

    def get_lambda(self):
        return self.lambda_
    
    
# -------------------------------------------------------------------------------------------------------------------------------------------------

# operand
class Rand:
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

# operator
class Rator:
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

# condition
class Beta:
    def __init__(self):
        self.data = "beta"
        
class Bool(Rand):
    def __init__(self, data):
        super().__init__(data)

# binary operatore
class Bop(Rator):
    def __init__(self, data):
        super().__init__(data)

class Uop(Rator):
    def __init__(self, data):
        super().__init__(data)

class Tau:
    def __init__(self, n):
        self.data = "tau"
        self.set_n(n)

    def set_n(self, n):
        self.n = n

    def get_n(self):
        return self.n

class Aug(Rand):
    def __init__(self):
        super().__init__("aug")
        self.symbols = []

# container that holds operations
class Container:
    def __init__(self):
        self.data = "b"
        self.symbols = []

class Id(Rand):
    def __init__(self, data):
        super().__init__(data)
    
    def get_data(self):
        return super().get_data()

class Int(Rand):
    def __init__(self, data):
        super().__init__(data)

class Str(Rand):
    def __init__(self, data):
        super().__init__(data)

class Ystar:
    def __init__(self):
        self.data = "<Y*>"

class Dummy(Rand):
    def __init__(self):
        super().__init__("dummy")