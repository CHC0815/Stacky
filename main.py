from src.nodes import *
from enum import Enum
from typing import List
import sys
import subprocess

from src.lexer import Lexer
from src.parser import Parser
from src.prog import Program


def simulate_program(prog: Program):
    while prog.index < len(prog.nodes):
        prog.nodes[prog.index].simulate(prog)
        prog.index += 1


def compile_program(prog: Program):
    filename = sys.argv[2].split('.')[0] + ".asm"
    with open(filename, 'w') as f:
        f.write("BITS 64\n")
        f.write("section .text\n")
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
        f.write(f'puts:\n')
        f.write(f'    mov rax, 0x1\n')
        f.write(f'    mov rdi, 0x1\n')
        # f.write(f'    mov rsi, address\n') move string address to rsi
        # f.write(f'    mov rdx, length\n') move string length to rdx
        f.write(f'    syscall\n')
        f.write(f'    ret\n')
        f.write(f'global _start\n')
        f.write(f'_start:\n')

        while prog.index < len(prog.nodes):
            asm = prog.nodes[prog.index].compile(prog)
            prog.index += 1
            f.write(asm)

        # exit
        f.write(f'; --- exit ---\n')
        f.write(f'    mov rax, 60\n')
        f.write(f'    mov rdi, 0\n')
        f.write(f'    syscall\n')

        # string content
        f.write(f'section .data\n')
        f.write(f';---- strings ----\n')
        for string in prog.strings:
            f.write(f'{string}\n')

        # counter variables
        f.write(f';---- counters ----\n')
        for counter in prog.counters:
            f.write(f'{counter} DQ 0\n')

    compile(filename)


def compile(filename: str):
    cmd = f'nasm -f elf64 {filename}'
    subprocess.run(cmd.split())
    link(filename.split('.')[0] + ".o")


def link(filename: str):
    cmd = f'ld -s -o {filename.split(".")[0]} {filename}'
    subprocess.call(cmd.split())


def main():
    lines = []
    path = sys.argv[2]
    with open(path, 'r') as f:
        lines = f.readlines()
    lexer = Lexer(path, lines)
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
