## 프로그램 흐름
    1. 무한반복문
    2. f p e case
    3. f->box 값 box크기만큼 문자열 입력
    4. p->박스[idx] 출력, idx지정 --> 카나리 유출가능
    5. e->이름 크기 지정 ,크기만큼 이름 입력 --> bof가능

## 보호기법
아키텍처 : i386
canary found
nx enabled
no pie

## 취약점
box라는 문자열의 인덱스로 출력하는 과정에서 카나리 유출 위험
이름 크기 사용자 지정해서 bof위험
p->박스[idx] 출력, idx지정 --> 카나리 유출가능
e->이름 크기 지정 ,크기만큼 이름 입력 --> bof가능

## 스택구조
rip     4bytes
rbp     4bytes  rbp
edi     4bytes  ebp-0x04  5 4 3 2
canary          rbp-0x08 131 130 129 128
name            ebp-0x48
box             ebp-0x88
select          ebp-8a
idx             rbp-0x90
name_len        ebp-0x94
argc            rbp-0x98

## 시나리오
f -> box 크기0x40 문자열 입력
p -> 0x42 43 44 반복문으로 카나리 유출
e -> 이름 크기 0x9c하여 전체 bof 공격

## 배운점
read(0, select, 2); 표준입력으로 2바이트 읽기
지역변수 스택 확인방법
    1. 선언 역순(항상 아님 c코드 보고 확인해야함) + 정렬
    2.b main -> disass main하고 ebp 혹은 rbp - 유심 관찰
cnry += bytes([byte])   b'\'이렇게 한바이트로 변환해준다

    