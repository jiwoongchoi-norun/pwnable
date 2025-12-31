data = open("execve.bin","rb").read()
print("shellcode = b\"" + "".join(f"\\x{x:02x}" for x in data) + "\"")