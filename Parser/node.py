class Node:
    def __init__(self, label, children=None):
        self.label = label
        if children is not None:
            self.children = children
        else:
            self.children = []

    # This function makes the tree print nicely with indentation
    def __repr__(self, level=0):
        result = "    " * level + str(self.label) + "\n"
        for child in self.children:
            result += child.__repr__(level + 1)
        return result





