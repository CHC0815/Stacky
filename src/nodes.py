from typing import List
from src.lexer import Token
from src.stack import Stack
from src.error import Error, NotEnoughOperantsError
from src.prog import Program


class Node():
    def __init__(self, token: Token) -> None:
        self.token = token

    def __str__(self) -> str:
        return str(self.token)

    def __repr__(self) -> str:
        return repr(self.token)

    def simulate(self, prog: Program):
        raise NotImplementedError()

    def compile(self, prog: Program) -> str:
        '''returns the x86 64 assembly for the current node'''
        raise NotImplementedError()
        return f';not implemenmted!!'


class NodeNumber(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        prog.stack.push(int(self.token.value))

    def compile(self, prog: Program) -> str:
        comp = f';--- push {self.token.value} to stack ---\n'
        comp += f'    mov rax, {self.token.value}\n'
        comp += f'    push rax\n'
        return comp

    def __str__(self) -> str:
        return f'NumberNode: {self.token.value}'

    def __repr__(self) -> str:
        return self.__str__()


class NodeAdd(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(a + b)

    def compile(self, prog: Program) -> str:
        comp = f';--- add two numbers ---\n'
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        comp += f'    add rax, rbx\n'
        comp += f'    push rax\n'
        return comp

    def __str__(self) -> str:
        return f'AddNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeSubtract(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(b - a)

    def compile(self, prog: Program) -> str:
        comp = f';--- subtract two numbers ---\n'
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        comp += f'    sub rbx, rax\n'
        comp += f'    push rax\n'
        return comp

    def __str__(self) -> str:
        return f'SubtractNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodePrint(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 1:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 1)
        a = prog.stack.pop()
        print(a)

    def compile(self, prog: Program) -> str:
        comp = f';--- print number ---\n'
        comp += f'    pop rdi\n'
        comp += f'    call print\n'
        return comp

    def __str__(self) -> str:
        return f'PrintNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeMultiply(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(a * b)

    def compile(self, prog: Program) -> str:
        comp = f';--- multiplies two numbers ---\n'
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        comp += f'    imul rax, rbx\n'
        comp += f'    push rax\n'
        return comp

    def __str__(self) -> str:
        return f'MultiplyNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeDivide(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(b / a)

    def compile(self, prog: Program) -> str:
        comp = f';--- divides two numbers ---\n'
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        comp += f'    idiv rax, rbx\n'
        comp += f'    push rax\n'
        return comp

    def __str__(self) -> str:
        return f'DivideNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeDupilcate(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        prog.stack.push(a)
        prog.stack.push(a)

    def compile(self, prog: Program) -> str:
        comp = f';--- dupilicates a number ---\n'
        comp += f'    pop rax\n'
        comp += f'    push rax\n'
        comp += f'    push rax\n'
        return comp

    def __str__(self) -> str:
        return f'DuplicateNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeSwap(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(a)
        prog.stack.push(b)

    def compile(self, prog: Program) -> str:
        comp = f';--- swapes two numbers ---\n'
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        comp += f'    push rax\n'
        comp += f'    push rax\n'
        return comp

    def __str__(self) -> str:
        return f'SwapNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeDrop(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 1:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 1)
        a = prog.stack.pop()

    def compile(self, prog: Program) -> str:
        comp = f';--- drops the first number ---\n'
        comp += f'    pop rax\n'
        return comp

    def __str__(self) -> str:
        return f'DropNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeEmit(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 1:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 1)
        a = prog.stack.pop()
        print(chr(int(a)))

    def compile(self, prog: Program) -> str:
        return super().compile()

    def __str__(self) -> str:
        return f'EmitNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeEquals(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(int(a == b))

    def compile(self, prog: Program) -> str:
        comp = f';--- checks for equality of two numbers ---\n'
        comp += f'    mov rcx, 0\n'  # false
        comp += f'    mov rdx, 1\n'  # true
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        comp += f'    cmp rax, rbx\n'
        comp += f'    cmove rcx, rdx\n'  # move if zero (equal)
        comp += f'    push rcx\n'

    def __str__(self) -> str:
        return f'EqualsNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeDebugStack(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        print(prog.stack)

    def compile(self, prog: Program) -> str:
        return super().compile()

    def __str__(self) -> str:
        return f'DebugStackNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeDebugDict(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        for k, v in prog.dict.items():
            print(f'{k} -> {v}\n')

    def compile(self, prog: Program) -> str:
        return super().compile()

    def __str__(self) -> str:
        return f'DebugDictNode'

    def __repr__(self) -> str:
        return super().__str__()


class NodeCall(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.name = token.value

    def simulate(self, prog: Program):
        for i in range(len(prog.dict[self.name])):
            prog.nodes.insert(prog.index + i + 1, prog.dict[self.name][i])

    def compile(self, prog: Program) -> str:
        return super().compile()

    def __str__(self) -> str:
        s = f'NodeCall:\n'
        s += f'    Name: {self.name}'
        return s

    def __repr__(self) -> str:
        return super().__str__()


class NodeWord(Node):
    def __init__(self, name: str, content: List[Token]) -> None:
        super().__init__(None)
        self.name = name
        self.content = content

    def simulate(self, prog: Program):
        prog.dict[self.name] = self.content

    def compile(self, prog: Program) -> str:
        return super().compile()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        s = f'NodeWord:\n'
        s += f'    Name: {self.name}\n'
        s += f'    Content:\n'
        for el in self.content:
            s += f'        {el}\n'
        return s
