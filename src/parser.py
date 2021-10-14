from typing import Dict, List, Tuple
from src.error import InvalidSyntaxError
from src.lexer import Token, TokenType
from src.nodes import *
from src.prog import Program


class Parser():
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    def advance(self):
        self.index += 1

    def get_token(self) -> Token:
        if(self.index < len(self.tokens)):
            return self.tokens[self.index]
        raise AttributeError()

    # ------------------

    def parse(self) -> Program:
        self.nodes: List[Node] = []
        self.dict = {'ADD': '+'}

        token = self.get_token()
        while token.tokenType != TokenType.EOF:
            self.nodes.append(self.get_node(token))
            self.advance()
            token = self.get_token()
        program = Program(self.nodes, self.dict)
        return program

    def is_conditional(self, token: Token):
        if token in [TokenType.OP_EQ, TokenType.OP_LT, TokenType.OP_GT]:
            return True
        return False

    def get_node(self, token) -> Node:
        if token == None:
            raise InvalidSyntaxError(token.file_name, token.line_number)
        if token.tokenType == TokenType.OP_NUMBER:
            return NodeNumber(token)
        elif token.tokenType == TokenType.OP_ADD:
            return NodeAdd(token)
        elif token.tokenType == TokenType.OP_SUB:
            return NodeSubtract(token)
        elif token.tokenType == TokenType.OP_PRINT:
            return NodePrint(token)
        elif token.tokenType == TokenType.OP_MUL:
            return NodeMultiply(token)
        elif token.tokenType == TokenType.OP_DIV:
            return NodeMultiply(token)
        elif token.tokenType == TokenType.OP_DUP:
            return NodeDupilcate(token)
        elif token.tokenType == TokenType.OP_SWAP:
            return NodeSwap(token)
        elif token.tokenType == TokenType.OP_DROP:
            return NodeDrop(token)
        elif token.tokenType == TokenType.OP_EMIT:
            return NodeEmit(token)
        elif token.tokenType == TokenType.OP_EQ:
            return NodeEquals(token)
        elif token.tokenType == TokenType.DEBUG_STACK:
            return NodeDebugStack(token)
        elif token.tokenType == TokenType.DEBUG_DICT:
            return NodeDebugDict(token)
        elif token.tokenType == TokenType.OP_COLON:
            self.advance()
            tok: Token = self.get_token()
            if tok == None:
                raise InvalidSyntaxError(tok.file_name, tok.file_number)
            name = tok.value

            if name[-1] == '?':
                # if then TODO: ELSE
                node = NodeIf(token, name)
                condition: List[Node] = []
                content: List[Node] = []
                else_case: List[Node] = []
                self.advance()  # advance name
                next: Token = self.get_token()

                while next.tokenType != TokenType.OP_IF:
                    condition.append(self.get_node(next))
                    self.advance()
                    next = self.get_token()

                self.advance()  # advance if
                next: Token = self.get_token()

                while next.tokenType != TokenType.OP_THEN and next.tokenType != TokenType.OP_ELSE:
                    content.append(self.get_node(next))
                    self.advance()
                    next = self.get_token()

                # no else case
                if next.tokenType == TokenType.OP_THEN:
                    self.advance()  # then
                    node.condition = condition
                    node.content = content
                    node.else_part = []
                    return node

                # else case
                self.advance()  # else
                next: Token = self.get_token()

                while next.tokenType != TokenType.OP_THEN:
                    else_case.append(self.get_node(next))
                    self.advance()
                    next = self.get_token()

                self.advance()  # then
                node.condition = condition
                node.content = content
                node.else_part = else_case
                return node

            else:
                # start word or loop
                is_loop = False
                content: List[Node] = []
                self.advance()  # advance name
                next: Token = self.get_token()
                while next.tokenType != TokenType.OP_SEMICOLON:
                    if next.tokenType == TokenType.OP_DO:
                        is_loop = True
                        break
                    content.append(self.get_node(next))
                    self.advance()
                    next = self.get_token()

                # return word node
                if not is_loop:
                    node = NodeWord(name, content)
                    self.dict[name] = node
                    return node

                # continue with loop node
                # content contains from to numbers
                self.advance()  # advance "do"
                next: Token = self.get_token()
                body: List[Node] = []
                while next.tokenType != TokenType.OP_LOOP:
                    body.append(self.get_node(next))
                    self.advance()
                    next = self.get_token()

                self.advance()  # advance "loop"

                node = NodeLoop(token, name, content, body)
                self.dict[name] = node
                return node

        elif token.tokenType == TokenType.OP_STRING:
            return NodeString(token)
        elif token.tokenType == TokenType.OP_PUTS:
            return NodePuts(token)
        elif token.tokenType == TokenType.OP_LT:
            return NodeLessThan(token)
        elif token.tokenType == TokenType.OP_GT:
            return NodeGreaterThan(token)
        elif token.tokenType == TokenType.OP_AND:
            return NodeAnd(token)
        elif token.tokenType == TokenType.OP_OR:
            return NodeOr(token)
        elif token.tokenType == TokenType.OP_INVERT:
            return NodeInvert(token)
        elif token.tokenType == TokenType.OP_MOD:
            return NodeMod(token)
        elif token.tokenType == TokenType.OP_CR:
            return NodeCarriageReturn(token)
        else:
            if token.value == None:
                print(token)
                raise Error(token.file_name, token.line_number)
            elif token.value[-1] == '?':
                return NodeCallIf(token)
            else:
                return NodeCall(token)
