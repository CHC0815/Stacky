from enum import Enum


class TokenType(Enum):
    OP_NUMBER = id()
    OP_ADD = id()
    OP_SUB = id()
    OP_PRINT = id()
    OP_MUL = id()
    OP_DIV = id()
    OP_DUP = id()
    OP_SWAP = id()
    OP_DROP = id()
    OP_EMIT = id()
    OP_WORD = id()
    OP_EQ = id()
    OP_COLON = id()
    OP_SEMICOLON = id()
    DEBUG_STACK = id()
    DEBUG_DICT = id()


class Token():
    def __init__(self, tokenType, value):
        self.tokenType = tokenType
        self.value = value

    def __str__(self) -> str:
        return f'{self.tokenType} : {self.value}'

    def __repr__(self) -> str:
        return f'{self.tokenType} : {self.value}'


class Program():
    def __init__(self):
        self.dict = []
        self.self.program = []

    def set_prog(self, prog):
        self.self.program = prog

    def add_word(self, word, value):
        self.dict[word] = value


class Lexer():
    def __init__(self, path):
        self.path = path
        self.lines = []
        self.program = []
        with open(path, 'r') as f:
            self.lines = f.readlines()

    def get_program(self):
        self.create_program()
        prog = Program()
        prog.set_prog(self.program)
        return prog

    def create_program(self):
        for line in self.lines:
            cmds = line.split()
            for cmd in cmds:
                if cmd.isdigit():
                    self.program.append(Token(TokenType.OP_NUMBER, int(cmd)))
                elif cmd == "ADD" or cmd == "+":
                    self.program.append(Token(TokenType.OP_ADD, None))
                elif cmd == "SUB" or cmd == "-":
                    self.program.append(Token(TokenType.OP_SUB, None))
                elif cmd == "PRINT" or cmd == ".":
                    self.program.append(Token(TokenType.OP_PRINT, None))
                elif cmd == "MUL" or cmd == "*":
                    self.program.append(Token(TokenType.OP_MUL, None))
                elif cmd == "DIV" or cmd == "/":
                    self.program.append(Token(TokenType.OP_DIV, None))
                elif cmd == "DUP":
                    self.program.append(Token(TokenType.OP_DUP, None))
                elif cmd == "SWAP":
                    self.program.append(Token(TokenType.OP_SWAP, None))
                elif cmd == "DROP":
                    self.program.append(Token(TokenType.OP_DROP, None))
                elif cmd == "EMIT":
                    self.program.append(Token(TokenType.OP_EMIT, None))
                elif cmd == "=":
                    self.program.append(Token(TokenType.OP_EQ, None))
                elif cmd == "STACK":
                    self.program.append(Token(TokenType.DEBUG_STACK, None))
                elif cmd == "DICT":
                    self.program.append(Token(TokenType.DEBUG_DICT, None))
                else:
                    self.program.append(Token(TokenType.OP_WORD, cmd))
