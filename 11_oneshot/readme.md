## 프로그램 흐름
라이브러리에 정의된 stdout변수의 주소를 출력시키고 msg변수에 bof가 되는 입력이 있습니다. check변수가 0보다 크면 프로그램을 종료하고 그 조건문이 거짓이라면 msg변수를 출력하고 프로그램이 종료되기전 msg변수부터 msg크기 만큼0으로 overwrite하고 종료된다.

## 보호기법 확인 
arch : amd64
no canary
nx enabled 
- 스택,힙 메모리에서 쉘코드 실행 불가
Partial RELRO
- .got .plt RW
PIE enabled
- base 주소가 계속 바뀐다

## 스택구조
rip             8바이트
rbp             8바이트
check rbp-0x8 8바이트
padding rbp-0x10  8바이트
msg   rbp-0x20  16바이트
argc    rbp-0x24
argv    rbp-0x30

## 취약점 확인
프로그램 내부에서 알수 있는 정보는 stdout의 주소
- libc 내부 전역 변수 주소 확보도니 libc_base 계산 가능
msg변수 입력으로 스택 구조 조작 가능
- check 8바이트 변수가 0보다 크면 종료 <- fake canary 역활
msg변수 크기 0으로 패딩되고 종료
==>stdout 유출 + ret overwrite ==one_gadget 가능

## ai 질문 사항
- size_t 바이트 : 32비트 4바이트 || 64비트 8바이트

## 배운점
0x45216 execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL
- rax 레지스터가 0이어야함
0x4526a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL <-이게 조건이 됨
0xf02a4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1147 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
- 점점 스택에서 멀어저 안전해지고 쉬워진다

- 프로그램 내부에서 라이브러리 변수의 주소가 주어지면 외부 라이브러리의 값을 뺴서 base값을 쉽게 구할수 있고 스택구조 ret를 overwrite할수 있는 상황에서 one_gadget를 준비해 공격하면 성공 가능성이 높다

- ret 주소를 one_gadget으로 덮어서
RIP가 libc 내부 execve('/bin/sh') 코드로 점프하게 만들고
코드 재사용 공격으로 쉘을 획득한다.