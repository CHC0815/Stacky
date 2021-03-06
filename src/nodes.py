from typing import List
from src.lexer import Token, TokenType
from src.stack import Stack
from src.error import Error, InvalidSyntaxError, NotDefinedError, NotEnoughOperantsError
from src.prog import Program


class Node():
    def __init__(self, token: Token) -> None:
        self.token = token

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'{self.token}'

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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'NumberNode: {self.token.value}'


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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'AddNode'


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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'SubtractNode'


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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'PrintNode'


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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'MultiplyNode'


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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'DivideNode'


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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'DuplicateNode'


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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'SwapNode'


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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'DropNode'


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
        return self.__repr__()

    def __repr__(self) -> str:
        return f'EmitNode'


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
        return comp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'EqualsNode'


class NodeDebugStack(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        print(prog.stack)

    def compile(self, prog: Program) -> str:
        return super().compile(prog)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'DebugStackNode'


class NodeDebugDict(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        for k, v in prog.dict.items():
            print(f'{k} -> {v}\n')

    def compile(self, prog: Program) -> str:
        return super().compile(prog)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'DebugDictNode'


# TODO: refactor NodeCall in own classes and functions
class NodeCall(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.name = token.value

    def simulate(self, prog: Program):
        if not self.name in prog.dict:
            raise NotDefinedError(self.token.file_name, self.token.line_number, self.name)
        node = prog.dict[self.name]

        if isinstance(node, NodeWord):
            for i in range(len(node)):
                prog.nodes.insert(prog.index + i + 1, node[i])

        elif isinstance(node, NodeLoop):
            self.content = node.content
            self.body = node.body

            # simulate loop body
            for el in self.content:
                el.simulate(prog)

            if len(prog.stack) < 2:
                raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)

            a = prog.stack.pop()  # begin
            b = prog.stack.pop()  # end
            self.counter = a

            while self.counter < b:
                # simulate body but check for Word "i" -> replace with self.counter

                for el in self.body:
                    if isinstance(el, NodeCall):
                        if el.name == "i":
                            token = Token(TokenType.OP_NUMBER, self.counter, "internal counter variable", -1)
                            node = NodeNumber(token)
                            node.simulate(prog)
                        else:
                            # normal
                            el.simulate(prog)
                    else:
                        el.simulate(prog)

                self.counter += 1

    def compile(self, prog: Program) -> str:
        if not self.name in prog.dict:
            raise NotDefinedError(self.token.file_name, self.token.line_number, self.name)
        node = prog.dict[self.name]

        if isinstance(node, NodeWord):
            for i in range(len(node)):
                prog.nodes.insert(prog.index + i + 1, node[i])
            return ""
        elif isinstance(node, NodeLoop):
            self.content = node.content
            self.body = node.body

            counter_start = prog.get_counter_label()
            counter_end = prog.get_counter_label()
            prog.counters.append(counter_start)
            prog.counters.append(counter_end)

            loop_start = prog.get_label()
            loop_body_start = prog.get_label()
            loop_end = prog.get_label()
            comp = f'; loop start\n'
            comp += f'{loop_start}:\n'
            for el in self.content:
                comp += el.compile(prog)
            # added content part ...

            # get from to numbers
            comp += f'    pop rax\n'  # start number
            comp += f'    mov [{counter_start}], rax\n'  # move start number in counter_start
            comp += f'    pop rax\n'  # end number
            comp += f'    mov [{counter_end}], rax\n'  # move start number in counter_end

            # body begin
            comp += f'; loop body begin\n'
            comp += f'{loop_body_start}:\n'
            for el in self.body:
                if isinstance(el, NodeCall):
                    if el.name == "i":
                        comp += f'    mov rax, [{counter_start}]\n'
                        comp += f'    push rax\n'
                    else:
                        comp += el.compile(prog)
                else:
                    comp += el.compile(prog)

            # count up
            comp += f'    mov rax, [{counter_start}]\n'
            comp += f'    inc rax\n'
            comp += f'    mov  [{counter_start}], rax\n'

            # check loop condition
            comp += f'    mov rax, [{counter_start}]\n'
            comp += f'    mov rbx, [{counter_end}]\n'
            comp += f'    cmp rax, rbx\n'
            comp += f'    jne {loop_body_start}\n'  # if not equal (-> less) jump back to body start

            comp += f';loop end\n'
            comp += f'{loop_end}:\n'
            comp += f'    nop\n'
            return comp

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
        prog.dict[self.name] = self.content
        return ""

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        s = f'NodeWord:\n'
        s += f'    Name: {self.name}\n'
        s += f'    Content:\n'
        for el in self.content:
            s += f'        {el}\n'
        return s


class NodeString(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.string = token.value

    def simulate(self, prog: Program):
        prog.strings.append(self.string[1:-1])
        index = len(prog.strings) - 1
        prog.stack.push(index)  # pointer
        prog.stack.push(len(self.string))  # length of string

    def compile(self, prog: Program) -> str:
        index = f'string_{len(prog.strings)}'  # string_0, string_1, ...
        prog.strings.append(f'{index}: db {self.string}')  # , 0x0a, 0x0d')
        comp = f';---- string ----\n'
        comp += f'    push {index}\n'  # push address
        comp += f'    push {len(self.string)}\n'
        return comp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        s = f'StringNode:\n'
        s += f'    String: {self.string}\n'
        return s


class NodePuts(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()  # length
        b = prog.stack.pop()  # pointer
        string = prog.strings[b]
        print(string)

    def compile(self, prog: Program) -> str:
        comp = f';--- prints string ---\n'
        comp += f'    pop rdx\n'  # length
        comp += f'    pop rsi\n'  # address / label
        comp += f'    call puts\n'
        return comp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'PutsNode'


class NodeLessThan(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(int(a > b))

    def compile(self, prog: Program) -> str:
        comp = f';--- checks for equality of two numbers ---\n'
        comp += f'    mov rcx, 0\n'  # true
        comp += f'    mov rdx, 1\n'  # false
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        comp += f'    cmp rax, rbx\n'
        comp += f'    cmovg rcx, rdx\n'  # move if greater than (the opposite)
        comp += f'    push rcx\n'
        return comp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'LessThanNode'


class NodeGreaterThan(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(int(a < b))

    def compile(self, prog: Program) -> str:
        comp = f';--- checks for equality of two numbers ---\n'
        comp += f'    mov rcx, 0\n'  # true
        comp += f'    mov rdx, 1\n'  # false
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        comp += f'    cmp rax, rbx\n'
        comp += f'    cmovl rcx, rdx\n'  # move if less than
        comp += f'    push rcx\n'
        return comp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'GreaterThanNode'


class NodeAnd(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(int(a and b))

    def compile(self, prog: Program) -> str:
        # compare and jump to false if false
        # if not jumped push 1 and jump to end
        comp = f';---- and ----\n'
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        comp += f'    cmp rax, 1\n'
        false = prog.get_label()
        comp += f'    jne {false}\n'
        comp += f'    cmp rbx, 1\n'
        comp += f'    jne {false}\n'
        comp += f'    push 1\n'         # true
        end = prog.get_label()
        comp += f'    jmp {end}\n'
        comp += f'{false}:\n'
        comp += f'    push 0\n'         # false
        comp += f'{end}:\n'
        comp += f'    nop\n'
        return comp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'AndNode'


class NodeOr(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(int(a or b))

    def compile(self, prog: Program) -> str:
        comp = f';---- or ----\n'
        comp += f'    pop rax\n'
        comp += f'    pop rbx\n'
        true = prog.get_label()
        end = prog.get_label()
        comp += f'    cmp rax, 1\n'
        comp += f'    je {true}\n'
        comp += f'    cmp rbx, 1\n'
        comp += f'    je {true}\n'
        comp += f'    push 0\n'
        comp += f'    jmp {end}\n'
        comp += f'{true}:\n'
        comp += f'    push 1\n'
        comp += f'{end}:\n'
        comp += f'    nop'
        return comp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'OrNode'


class NodeInvert(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 1:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 1)
        a = prog.stack.pop()
        prog.stack.push(int(not a))

    def compile(self, prog: Program) -> str:
        return super().compile(prog)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'InvertNode'


class NodeMod(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        if len(prog.stack) < 2:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, 2)
        a = prog.stack.pop()
        b = prog.stack.pop()
        prog.stack.push(int(b % a))

    def compile(self, prog: Program) -> str:
        comp = f';---- mod ----\n'
        comp += f'    xor rax, rax\n'
        comp += f'    xor rdx, rdx\n'
        comp += f'    pop rbx\n'
        comp += f'    pop rax\n'    # divide rax by rbx
        comp += f'    div rbx\n'
        # remainder stored in rdx
        comp += f'    push rdx\n'
        return comp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'ModNode'


class NodeIf(Node):
    def __init__(self, token: Token, name: str) -> None:
        super().__init__(token)
        self.name = name
        self.condition: List[Node] = []
        self.content: List[Node] = []
        self.else_part: List[Node] = []

    def simulate(self, prog: Program):
        prog.dict[self.name] = (self.condition, self.content, self.else_part)

    def compile(self, prog: Program) -> str:
        prog.dict[self.name] = (self.condition, self.content, self.else_part)
        return ''

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        s = f'CallIfNode:\n'
        s += f'    Condition:\n'
        for el in self.condition:
            s += f'        {el}\n'
        s += f'    If Part:\n'
        for el in self.content:
            s += f'        {el}\n'
        s += f'    Else Part:\n'
        for el in self.else_part:
            s += f'        {el}\n'

        return s


class NodeCallIf(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.name = self.token.value
        self.condition = []
        self.content = []
        self.else_part = []

    def simulate(self, prog: Program):
        if not self.name in prog.dict:
            raise NotDefinedError(self.token.file_name, self.token.line_number, self.name)

        self.condition = prog.dict[self.name][0]
        self.content = prog.dict[self.name][1]
        self.else_part = prog.dict[self.name][2]

        if self.condition == []:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, -1)
        # add condition part
        for i in range(len(self.condition)):
            self.condition[i].simulate(prog)

        # last thing on the stack must be 0 or 1
        a = prog.stack.pop()
        if a != 0 and a != 1:
            raise InvalidSyntaxError(self.token.file_name, self.token.line_number, self.token)

        if a == 1:
            for i in range(len(self.content)):
                prog.nodes.insert(prog.index + i + 1, self.content[i])
        else:
            for i in range(len(self.else_part)):
                prog.nodes.insert(prog.index + i + 1, self.else_part[i])

    def compile(self, prog: Program) -> str:
        self.condition = prog.dict[self.name][0]
        self.content = prog.dict[self.name][1]
        self.else_part = prog.dict[self.name][2]

        if self.condition == []:
            raise NotEnoughOperantsError(self.token.file_name, self.token.line_number, -1)
        comp = f';---- if node ----\n'
        for el in self.condition:
            comp += el.compile(prog)

        comp += f'    pop rax\n'
        comp += f'    cmp rax, 1\n'  # true
        else_part = prog.get_label()
        comp += f'    jne {else_part}\n'

        end = prog.get_label()
        # true part
        for el in self.content:
            comp += el.compile(prog)
        comp += f'    jmp {end}\n'

        # else part
        comp += f'{else_part}:\n'
        for el in self.else_part:
            comp += el.compile(prog)

        comp += f'{end}:\n'
        comp += f'    nop\n'

        return comp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        s = f'CallIfNode:\n'
        s += f'    Name: {self.name}\n'
        return s


class NodeLoop(Node):
    def __init__(self, token: Token, name: str,  content: List[Node], body: List[Node]) -> None:
        super().__init__(token)
        self.name = name
        self.content = content
        self.body = body
        self.counter = 0

    def simulate(self, prog: Program):
        pass

    def compile(self, prog: Program) -> str:
        return f''

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        s = f'LoopNode:\n'
        s += f'    Content:\n'
        for el in self.content:
            s += f'        {el}\n'
        s += f'    Body:\n'
        for el in self.body:
            s += f'        {el}\n'

        return s


class NodeCarriageReturn(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def simulate(self, prog: Program):
        string_token = Token(TokenType.OP_STRING, "\n", "internal", -1)
        a = NodeString(string_token)
        a.simulate(prog)

    def compile(self, prog: Program) -> str:
        # TODO: implement
        return super().compile(prog)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'CarriageReturnNode'
