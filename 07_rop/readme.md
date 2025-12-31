## 프로그램 흐름
    카나리 유출 목적 입력 명령이 있고 카나리를 가지고 rop 입력을 받는 명령으로 구성되어 있다

## 보호기법 확인
arch : amd64
canary found
nx enabled
no pie

## 스택구조 확인
rip 8바이트
rbp 8바이트
canary 8바이트 rbp-0x8
dummy 2바이트 rbp-0x10  
buf 0x30바이트 rbp-0x40

## 공격 악성코드 준비물
스택 메모리에서는 실행 불가
라이브러리 영역에서 실행을 시켜야한다
**마지막 rip영역 필요한 코드** write,read를 쓴다 생각하면 필수
    ret조각 = 0x400596 --> 마지막 스택 구조 맞추기 위해
    pop rdi 조각 = 0x400853
        ㄴROPgadget --binary rop | egrep "pop rdi"
        ㄴ read write첫번쨰 인자가 필수이기에
    pop rsi = 0x400851 
        ㄴ read write의 버퍼 혹은 주소가 되기에 미리 준비 필수

## exploit 흐름
바이너리에서 실행되는 함수의 주소를 알기위해 ELF("./rio")명령을 가져오고 주어진 라이브러리 파일의 고정주소에서 오프셋이 더해지는 기준 주소를 알기위해 가져온다
리턴가젯을 만들기위해 plt['read'] plt['write'] got['read'] got['write']를 가져온다 여기서 got는 실행중 실제 libc함수 주소가 저장되는 메모리 위치이고 plt는 함수를 호출하기위한 바이너리 내부 코드 주소이다
그리고 패딩 해서 카나리 유출 시킨다
rip 조작 코드
1. 우선적으로 우리가 알수 있는 read_got를 출력시켜서 - 라이브러리read주소로 계산하면 libc_base(라이브러리 기준 주소(오프셋))이 구해진다
그럼 system함수의 주소를 알수 있다
2. read_plt로 read_got의 주소를 덮는다. system주소와 그 뒤 /bin/sh로 덮으면 read_got는 system함수가 되고 그 뒤 연속적으로 /bin/sh값이 있다
3.함수의 첫번쨰 인자로 rdi값에 read주소의+0x8을 해서 /bin/sh의 주소를 받고 조작된 read_plt로 함수를 호출하면 라이브러리 주소들의 함수가 실행되어 system("./bin/sh")가 라이브러리에서 실행된다

*