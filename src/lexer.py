from enum import Enum
import shlex

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
    OP_LT = id()
    OP_GT = id()
    OP_COLON = id()
    OP_SEMICOLON = id()
    DEBUG_STACK = id()
    DEBUG_DICT = id()
    EOF = id()
    OP_IF = id()
    OP_THEN = id()
    OP_ELSE = id()
    OP_IF_WORD = id()
    OP_PUTS = id()
    OP_STRING = id()
    OP_AND = id()
    OP_OR = id()
    OP_INVERT = id()
    OP_MOD = id()
    OP_DO = id()
    OP_LOOP = id()
    OP_CR = id()


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
    def __init__(self, path, lines):
        self.path = path
        self.lines = lines
        self.program = []

    def get_program(self):
        self.create_program()
        self.program.append(Token(TokenType.EOF, None, self.path, -1))
        return self.program

    def create_program(self):
        self.line_counter = 1
        for line in self.lines:
            cmds = shlex.split(line, posix=False)
            for cmd in cmds:
                if cmd.isdigit():
                    self.cmd_number(cmd)
                elif cmd == "+":
                    self.cmd_add(cmd)
                elif cmd == "-":
                    self.cmd_sub(cmd)
                elif cmd == ".":
                    self.cmd_print(cmd)
                elif cmd == "*":
                    self.cmd_mul(cmd)
                elif cmd == "/":
                    self.cmd_div(cmd)
                elif cmd == "DUP" or cmd == "dup":
                    self.cmd_dup(cmd)
                elif cmd == "SWAP" or cmd == "swap":
                    self.cmd_swap(cmd)
                elif cmd == "DROP" or cmd == "drop":
                    self.cmd_drop(cmd)
                elif cmd == "EMIT" or cmd == "emit":
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
                elif cmd == "if":
                    self.cmd_if(cmd)
                elif cmd == "then" or cmd == "end":
                    self.cmd_then(cmd)
                elif cmd == "else":
                    self.cmd_else(cmd)
                elif cmd == "puts":
                    self.cmd_puts(cmd)
                elif cmd == ">":
                    self.cmd_gt(cmd)
                elif cmd == "<":
                    self.cmd_lt(cmd)
                elif cmd == "and":
                    self.cmd_and(cmd)
                elif cmd == "or":
                    self.cmd_or(cmd)
                elif cmd == "invert":
                    self.cmd_invert(cmd)
                elif cmd == "mod":
                    self.cmd_mod(cmd)
                elif cmd == "do":
                    self.cmd_do(cmd)
                elif cmd == "loop":
                    self.cmd_loop(cmd)
                elif cmd == "cr":
                    self.cmd_cr(cmd)
                else:
                    if cmd[-1] == '?':
                        self.cmd_if_word(cmd)
                    elif cmd[0] == '"' and cmd[-1] == '"':
                        self.cmd_string(cmd)
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

    def cmd_if(self, cmd):
        self.program.append(Token(TokenType.OP_IF, None, self.path, self.line_counter))

    def cmd_then(self, cmd):
        self.program.append(Token(TokenType.OP_THEN, None, self.path, self.line_counter))

    def cmd_if_word(self, cmd):
        self.program.append(Token(TokenType.OP_IF_WORD, cmd, self.path, self.line_counter))

    def cmd_puts(self, cmd):
        self.program.append(Token(TokenType.OP_PUTS, None, self.path, self.line_counter))

    def cmd_string(self, cmd):
        self.program.append(Token(TokenType.OP_STRING, cmd, self.path, self.line_counter))

    def cmd_lt(self, cmd):
        self.program.append(Token(TokenType.OP_LT, None, self.path, self.line_counter))

    def cmd_gt(self, cmd):
        self.program.append(Token(TokenType.OP_GT, None, self.path, self.line_counter))

    def cmd_and(self, cmd):
        self.program.append(Token(TokenType.OP_AND, None, self.path, self.line_counter))

    def cmd_or(self, cmd):
        self.program.append(Token(TokenType.OP_OR, None, self.path, self.line_counter))

    def cmd_invert(self, cmd):
        self.program.append(Token(TokenType.OP_INVERT, None, self.path, self.line_counter))

    def cmd_mod(self, cmd):
        self.program.append(Token(TokenType.OP_MOD, None, self.path, self.line_counter))

    def cmd_else(self, cmd):
        self.program.append(Token(TokenType.OP_ELSE, None, self.path, self.line_counter))

    def cmd_do(self, cmd):
        self.program.append(Token(TokenType.OP_DO, None, self.path, self.line_counter))

    def cmd_loop(self, cmd):
        self.program.append(Token(TokenType.OP_LOOP, None, self.path, self.line_counter))

    def cmd_cr(self, cmd):
        self.program.append(Token(TokenType.OP_CR, None, self.path, self.line_counter))
