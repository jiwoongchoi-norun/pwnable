## nx&aslr
aslr : 바이너리가 실행 될때마다 스택,힙,공유 라이브러리 등을 임의의 주소에 할당하는 보호 기법이다

## 보호 기법
   arch : amd64
   canary found
   NX enabled
   no pie

## 프로그램 흐름
  system("echo 'system@plt'");
  위 명령으로 터미널에 system@plt 출력되면서 카나리 유출 위한 buf을 입력받고 입력된값을 출력시키고 스택을 조작하기위해 buf를 입력받는다.

## 스택 구조 확인
rip      8bytes
rbp      8bytes
canary   8bytes   rbp-0x08
패딩      2       rbp-10
buf      0x30    rbp-0x40

## 문제점
카나리에 00바이트 끝인 바이트가 있어서 완전히 다 유출이 안됨 

## 시나리오
처음 입력하고 입력한값이 출력될때 카나리값을 얻고 리턴가젯을 활용해 쉘을 얻어오자

## 문제 해결 과정
이 문제에서는 nx가 켜져있어 ret2shellcode 공격이 안된다
우선적으로 스택 구조를 확인하고 카나리 유출 하여 값을 저장한다
그다음이 문제다
스택 힙 메모리에서는 실행이 안되므로 코드영역(./text) 혹은 라이브러리 영역에서 실행시켜야한다
코드에 /bin/sh도 있고 system도있으므로 rop공격을 실행해본다
rip에 ret로 밑으로 나오는 값들을 16바이트로 정렬시키게 한다
   ㄴ**objdump -d rtl | egrep "ret"**
그리고 system함수의 인자를 우리가 설정해야한다
   ㄴ**gdb들어가자마자 p system**
pop rdi를 쓰고 인자값인 /bin/sh 주소를 설정한다
   ㄴ**ROPgadget --binary ./rtl --re "pop rdi" + b main 후에 search /bin/sh확인**
그리고 마지막에 system함수 주소를 넣어 조작한다

## 배운점
1. 정적링크 : c파일 안에 라이브러리
   동적링크 : 같은 폴더 안에 라이브러리파일
   정적링크
    ㄴ 주소값 임의로 로드가 아니라 aslr 영향없음
    