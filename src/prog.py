from src.stack import Stack


class Program():
    def __init__(self, nodes, dict):
        self.nodes = nodes
        self.dict = dict
        self.stack = Stack()
        self.index = 0
