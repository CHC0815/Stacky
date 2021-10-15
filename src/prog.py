from src.stack import Stack


class Program():
    def __init__(self, nodes, dict):
        self.nodes = nodes
        self.dict = dict
        self.stack = Stack()
        self.index = 0
        self.strings = []
        self.counters = []
        self.label_counter = 0
        self.counter_variable_counter = 0

    def get_label(self) -> str:
        label = f'.L{self.label_counter}'
        self.label_counter += 1
        return label

    def get_counter_label(self) -> str:
        label = f'Counter_{self.counter_variable_counter}'
        self.counter_variable_counter += 1
        return label
