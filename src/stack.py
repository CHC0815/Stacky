from typing import List


class Stack():
    def __init__(self) -> None:
        self.stack: List[int] = []

    def pop(self) -> int:
        return self.stack.pop()

    def push(self, value: int) -> None:
        self.stack.append(value)

    def __str__(self) -> str:
        s = f'------------\n'
        for el in self.stack:
            s += f'{str(el)}\n'
        s += f'------------\n'
        return s

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self):
        return len(self.stack)
