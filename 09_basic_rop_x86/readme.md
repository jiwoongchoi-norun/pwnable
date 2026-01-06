## 프로그램 흐름
buf변수가 생성되고 초기화가 됩니다
bof가 가능한 read함수가 호출되고 buf변수의 값을 출력하는 프로그램이다

## 보호 기법
arch = i386
no canary
nx enabled
- 스택 쉘코드 실행 불가, ret2libc/ROP 필수 
no pie + partial relro
- 바이너리 코드/가젯 주소 고정 + got overwrite 가능(라이브러리 읽고 쓰기 권한)
## 취약점
스택 보호 기법 canary 없음
read함수에서 stack bof발생
nx우회해서 라이브러리에서 system("/bin/sh") 호출 가능

## 스택 구조
eip 4bytes
ebp 4bytes
edi ebp-0x4 4바이트
buf ebp-0x44 

## 시나리오
스택 패딩 이후 eip영역에서 read함수 got주소를 유출 시켜서 라이브러리offset 확인한다
system()함수 주소로 write_got주소 조작하고 write_plt실행->system("/bin/sh") 쉘 획득

## 리턴 가젯
0x080483c2 : ret
0x08048688 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret

## 치팅
32비트 함수 인자 가젯
0x08048688 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret
ㄴ 인수4개 함수 호출 시
0x0804868a : pop edi ; pop ebp ; ret
ㄴ 인자 2개 호출시 유연성 떨어진다
0x08048689 : pop esi ; pop edi ; pop ebp ; ret
ㄴ 인자 3개 호출시

## 배운점
32비트 함수 호출 스택 구조 (cdecl)

함수가 시작될 때 스택은 항상 이렇게 생김

ESP →
[ return address ] <-pop 가젯 
[ arg1 ]
[ arg2 ]
[ arg3 ]

bss = e.bss()
- 실행 시 메모리에 로드되는 전역 변수 영역(.bss)의 주소이다
- elf바이너리의 .bss 섹션 시작 주소로 rop에서 문자열이나 임시 데이터를 저장하기 위한 안정적인 rw메모리 영역이다

r.recvuntil(b'a'*0x40) #출력의 대상이 buf변수에 한하기에 그다음은 우리가 설정
read_addr=u32(r.recvn(4))
- 스택 조작시에 아무리 카나리 위까지 조작하더라도 변수만 출력이 기본이다. 

payload += p32(write_plt)
payload += b'A' * 0x4
payload += p32(bss)
- 마지막 조작된 함수 호출하는 과정이 64비트와 다르게 추가 되는 이유는 함수 호출 구조가 return address가 반드시 존재해야하기에 이 구절을 추가 해야한다