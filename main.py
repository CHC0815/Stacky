from src.nodes import *
from enum import Enum
import parser
from typing import List
import sys
import subprocess

from src.error import Error, NotEnoughOperantsError
from src.lexer import TokenType, Token, Lexer
from src.stack import Stack
from src.parser import Program, Parser


def simulate_program(prog: Program):
    stack = Stack()
    for node in prog.nodes:
        node.simulate(stack)
    print("Simulated")


def compile_program(prog):
    program = prog.program
    filename = sys.argv[2].split('.')[0] + ".asm"
    with open(filename, 'w') as f:
        f.write("BITS 64\n")
        f.write("segment .text\n")
        f.write("print:\n")
        f.write("    mov r9, -3689348814741910323\n")
        f.write("    sub rsp, 40\n")
        f.write("    mov BYTE [rsp+31], 10\n")
        f.write("    lea rcx, [rsp+30]\n")
        f.write(".L2:\n")
        f.write("    mov rax, rdi\n")
        f.write("    lea r8, [rsp+32]\n")
        f.write("    mul r9\n")
        f.write("    mov rax, rdi\n")
        f.write("    sub r8, rcx\n")
        f.write("    shr rdx, 3\n")
        f.write("    lea rsi, [rdx+rdx*4]\n")
        f.write("    add rsi, rsi\n")
        f.write("    sub rax, rsi\n")
        f.write("    add eax, 48\n")
        f.write("    mov BYTE [rcx], al\n")
        f.write("    mov rax, rdi\n")
        f.write("    mov rdi, rdx\n")
        f.write("    mov rdx, rcx\n")
        f.write("    sub rcx, 1\n")
        f.write("    cmp rax, 9\n")
        f.write("    ja  .L2\n")
        f.write("    lea rax, [rsp+32]\n")
        f.write("    mov edi, 1\n")
        f.write("    sub rdx, rax\n")
        f.write("    xor eax, eax\n")
        f.write("    lea rsi, [rsp+32+rdx]\n")
        f.write("    mov rdx, r8\n")
        f.write("    mov rax, 1\n")
        f.write("    syscall\n")
        f.write("    add rsp, 40\n")
        f.write("    ret\n")
        f.write(f'global _start\n')
        f.write(f'_start:\n')
        for el in program:
            if el.tokenType == TokenType.OP_NUMBER:
                f.write(f';--- push {el.value} to stack ---\n')
                f.write(f'    mov rax, {el.value}\n')
                f.write(f'    push rax\n')
            elif el.tokenType == TokenType.OP_ADD:
                f.write(f';--- add two numbers ---\n')
                f.write(f'    pop rax\n')
                f.write(f'    pop rbx\n')
                f.write(f'    add rax, rbx\n')
                f.write(f'    push rax\n')
            elif el.tokenType == TokenType.OP_SUB:
                f.write(f';--- subtract two numbers ---\n')
                f.write(f'    pop rax\n')
                f.write(f'    pop rbx\n')
                f.write(f'    sub rbx, rax\n')
                f.write(f'    push rax\n')
            elif el.tokenType == TokenType.OP_PRINT:
                f.write(f';--- print number ---\n')
                f.write(f'    pop rdi\n')
                f.write(f'    call print\n')
            elif el.tokenType == TokenType.OP_MUL:
                f.write(f';--- multiplies two numbers ---\n')
                f.write(f'    pop rax\n')
                f.write(f'    pop rbx\n')
                f.write(f'    imul rax, rbx\n')
                f.write(f'    push rax\n')
            elif el.tokenType == TokenType.OP_DIV:
                f.write(f';--- divides two numbers ---\n')
                f.write(f'    pop rax\n')
                f.write(f'    pop rbx\n')
                f.write(f'    idiv rax, rbx\n')
                f.write(f'    push rax\n')
            elif el.tokenType == TokenType.OP_DUP:
                f.write(f';--- dupilicates a number ---\n')
                f.write(f'    pop rax\n')
                f.write(f'    push rax\n')
                f.write(f'    push rax\n')
            elif el.tokenType == TokenType.OP_SWAP:
                f.write(f';--- swapes two numbers ---\n')
                f.write(f'    pop rax\n')
                f.write(f'    pop rbx\n')
                f.write(f'    push rax\n')
                f.write(f'    push rax\n')
            elif el.tokenType == TokenType.OP_DROP:
                f.write(f';--- drops the first number ---\n')
                f.write(f'    pop rax\n')
            elif el.tokenType == TokenType.OP_EMIT:
                f.write(f';--- prints the number as ascii ---\n')
                # TODO: emit x86 64 assembly for emit
            elif el.tokenType == TokenType.OP_EQ:
                f.write(f';--- checks for equality of two numbers ---\n')
                f.write(f'    mov rcx, 0\n')  # false
                f.write(f'    mov rdx, 1\n')  # true
                f.write(f'    pop rax\n')
                f.write(f'    pop rbx\n')
                f.write(f'    cmp rax, rbx\n')
                f.write(f'    cmove rcx, rdx\n')  # move if zero (equal)
                f.write(f'    push rcx\n')
            elif el.tokenType == TokenType.DEBUG_STACK:
                assert False, "Will not be implemented!"
            elif el.tokenType == TokenType.DEBUG_DICT:
                assert False, "Will not be implemented!"
            else:
                assert False, f'Something went wrong filename: {sys.argv[2]}/{el.line_number}'

        f.write(f'; --- exit ---\n')
        f.write(f'    mov rax, 60\n')
        f.write(f'    mov rdi, 0\n')
        f.write(f'    syscall\n')
    compile(filename)


def compile(filename: str):
    cmd = f'nasm -f elf64 {filename}'
    subprocess.run(cmd.split())
    link(filename.split('.')[0] + ".o")


def link(filename: str):
    cmd = f'ld -s -o {filename.split(".")[0]} {filename}'
    subprocess.call(cmd.split())


def main():
    lexer = Lexer(sys.argv[2])
    tokens = lexer.get_program()
    with open('./debug/lexer', 'w') as f:
        for tok in tokens:
            f.write(f'{tok}\n')
    parser = Parser(tokens)
    program = parser.parse()
    with open('./debug/parser', 'w') as f:
        for node in program.nodes:
            f.write(f'{node}\n')
    if sys.argv[1] == "sim":
        simulate_program(program)
    elif sys.argv[1] == "com":
        compile_program(program)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if(sys.argv[1] == "--help" or sys.argv[1] == "-h"):
            print("usage: python3 main.py [sim/com] file")
            print("sim : simulates the input file")
            print("com : compiles the input file to x86 64 assembly and linkes it.")
            print("")
            print("In simulation mode you will get error handling.")
            quit()
    elif len(sys.argv) < 3:
        print("Not enough parameters. Try --help")
        quit()

    if(sys.argv[1] != "sim" and sys.argv[1] != "com"):
        print("First argument must be sim or com. Check python3 main.py --help")
        quit()
    main()
