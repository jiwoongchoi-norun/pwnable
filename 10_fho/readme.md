## 보호 기법
arch = amd64
canary found
- 스택 보호 기법 있음
nx enabled
- 스택 힙 메모리 영역 쉘코드 실행 불가
full RELRO 
- got 읽기 전용, ret2libc,got overwrite 불가
PIE Enabled
- 바이너리 베이스 주소 매 실행마다 랜덤

## 프로그램 흐름
buf변수가 0x30바이트로 정의 되고 read함수로 0x100크기만큼 overflow할수 있는 첫 입력이 있다

addr이 주소가 되고 그의 해당하는 임의의 값을 입력한다
value의 주소가 addr의 값

addr의 주소를 입력하면 해당하는 주소의 메모리 해제기능이다

## 스택 구조
rip 8bytes **libc 주소**
ㄴ 여기서 __libc_start_call_main을 호출
rbp 8bytes **스택주소**
canary  8bytes  rbp-0x08
dummpy  8bytes  0x09~0x10
buf     0x30바이트  rbp-0x40
value   8바이트     rbp-0x48(41~48)
addr    8바이트     rbp-0x50(49~4a~50)

            
 
## 시나리오
PIE enabled + full relro이기에 rop,ret2libc 공격이 안된다.
그래서 새로 hook overwrite공격을 한다
_free_hook,system함수,"/bin/sh"의 오프셋
_free_hook = 0x3ed8e8   .bss
system = 0x4f550        .text
/bin/sh = 0x1b3e1a      .rodata


## 배운점
full relro
- got 읽기 전용, got overwrite 불가
- ret2libc 불가

PIE Enabled
- 바이너리 베이스 주소 매 실행마다 랜덤
- rop 가젯 주소 전부랜덤
- ret 가젯 주소 하드 코딩 불가

커널이 하는 일
- ELF 헤더 파싱
- 메모리 맵 생성
- 코드(text)
데이터
libc (ld-linux)
- 유저 스택 생성
argv
envp
auxv
초기 RIP / RSP 설정

- one shot gadget

- glibc 버전에 다른 함수 호출 규약(rip)




## 흐름
- 커널이 execve를 통해 프로그램 실행을 준비하고
ELF와 라이브러리를 매핑한 뒤
유저 모드에서 _start를 실행한다.
_start는 __libc_start_main을 호출하고,
__libc_start_call_main에서 call main을 하면서
return address(__libc_start_call_main+offset)가
유저 스택에 push된다.
이후 main 함수에 진입하면
함수 프롤로그가 실행되며 push rbp로
새로운 스택 프레임이 만들어진다.