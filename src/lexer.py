from enum import Enum

counter = 0


def id():
    global counter
    counter += 1
    return counter


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
    EOF = id()


class Token():
    def __init__(self, tokenType, value, file_name, line_number):
        self.tokenType = tokenType
        self.value = value
        self.line_number = line_number
        self.file_name = file_name

    def __str__(self) -> str:
        return f'{self.tokenType} : {self.value}'

    def __repr__(self) -> str:
        return f'{self.tokenType} : {self.value}'


class Lexer():
    def __init__(self, path):
        self.path = path
        self.lines = []
        self.program = []
        with open(path, 'r') as f:
            self.lines = f.readlines()

    def get_program(self):
        self.create_program()
        self.program.append(Token(TokenType.EOF, None, self.path, -1))
        return self.program

    def create_program(self):
        self.line_counter = 1
        for line in self.lines:
            cmds = line.split()
            for cmd in cmds:
                if cmd.isdigit():
                    self.cmd_number(cmd)
                elif cmd == "+":
                    self.cmd_add(cmd)
                elif cmd == "-":
                    self.cmd_sub(cmd)
                elif cmd == "PRINT" or cmd == ".":
                    self.cmd_print(cmd)
                elif cmd == "*":
                    self.cmd_mul(cmd)
                elif cmd == "/":
                    self.cmd_div(cmd)
                elif cmd == "DUP":
                    self.cmd_dup(cmd)
                elif cmd == "SWAP":
                    self.cmd_swap(cmd)
                elif cmd == "DROP":
                    self.cmd_drop(cmd)
                elif cmd == "EMIT":
                    self.cmd_emit(cmd)
                elif cmd == ":":
                    self.cmd_colon(cmd)
                elif cmd == ";":
                    self.cmd_semicolon(cmd)
                elif cmd == "=":
                    self.cmd_eq(cmd)
                elif cmd == "STACK":
                    self.cmd_stack(cmd)
                elif cmd == "DICT":
                    self.cmd_dict(cmd)
                else:
                    self.cmd_word(cmd)
        self.line_counter += 1
    # --------------------------

    def cmd_number(self, cmd):
        self.program.append(Token(TokenType.OP_NUMBER, int(cmd), self.path, self.line_counter))

    def cmd_add(self, cmd):
        self.program.append(Token(TokenType.OP_ADD, None, self.path, self.line_counter))

    def cmd_sub(self, cmd):
        self.program.append(Token(TokenType.OP_SUB, None, self.path, self.line_counter))

    def cmd_mul(self, cmd):
        self.program.append(Token(TokenType.OP_MUL, None, self.path, self.line_counter))

    def cmd_div(self, cmd):
        self.program.append(Token(TokenType.OP_DIV, None, self.path, self.line_counter))

    def cmd_dup(self, cmd):
        self.program.append(Token(TokenType.OP_DUP, None, self.path, self.line_counter))

    def cmd_swap(self, cmd):
        self.program.append(Token(TokenType.OP_SWAP, None, self.path, self.line_counter))

    def cmd_drop(self, cmd):
        self.program.append(Token(TokenType.OP_DROP, None, self.path, self.line_counter))

    def cmd_emit(self, cmd):
        self.program.append(Token(TokenType.OP_EMIT, None, self.path, self.line_counter))

    def cmd_eq(self, cmd):
        self.program.append(Token(TokenType.OP_EQ, None, self.path, self.line_counter))

    def cmd_stack(self, cmd):
        self.program.append(Token(TokenType.DEBUG_STACK, None, self.path, self.line_counter))

    def cmd_dict(self, cmd):
        self.program.append(Token(TokenType.DEBUG_DICT, None, self.path, self.line_counter))

    def cmd_print(self, cmd):
        self.program.append(Token(TokenType.OP_PRINT, None, self.path, self.line_counter))

    def cmd_word(self, cmd):
        self.program.append(Token(TokenType.OP_WORD, cmd, self.path, self.line_counter))

    def cmd_colon(self, cmd):
        self.program.append(Token(TokenType.OP_COLON, None, self.path, self.line_counter))

    def cmd_semicolon(self, cmd):
        self.program.append(Token(TokenType.OP_SEMICOLON, None, self.path, self.line_counter))
