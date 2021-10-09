from typing import Dict, List, Tuple
from src.error import InvalidSyntaxError
from src.lexer import Token, TokenType
from src.nodes import *
from src.program import Program


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
        nodes: List[Node] = []
        self.dict = {'ADD': '+'}

        token = self.get_token()
        while token.tokenType != TokenType.EOF:
            nodes.append(self.get_node(token))
            self.advance()
            token = self.get_token()
        program = Program(nodes, self.dict)
        return program

    def get_node(self, token) -> Node:
        print(token)
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
            content: List[Node] = []

            self.advance()
            next: Token = self.get_token()
            while next.tokenType != TokenType.OP_SEMICOLON:
                content.append(self.get_node(next))
                self.advance()
                next = self.get_token()

            # self.advance()  # advance semicolon
            node = NodeWord(name, content)
            self.dict[name] = node
            return node
        else:
            return NodeCall(token)
