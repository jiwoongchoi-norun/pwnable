## 프로그램 흐름
    read함수로 buf변수 입력을 받고 write함수로 buf크기만큼 출력이 된다

## 보호기법
arch : amd64
no canary
nx enavled
no pie

## 스택구조
rip     rbp+0x8         8바이트
sfp     rbp            8바이트
buf     rbp-0x40        0x40바이트        
padding        rbp-0x50

## 취약점 -> 공격
read함수의 입력 크기 값이 buf변수보다 훨씬 더 크기에 bof 발생한다
rip를 조작시켜 쉘을 가져올것이다

## 공격 발상 흐름
bof시켜 rip를 조작한다
주어진 자료는 실행파일의 바이너리 파일을 확인 가능하고 라이브러리 파일이 존재한다
어느 한 바이너리 함수 주소를 알면 라이브러리 주소값과 빼면 오프셋이 구해지고 system("/bin/sh")함수 주소를 호출하며 nx우회하여 실행시킨다

## 공격 준비도구
pop rdi     0x400883
pop rsi     0x400881
ret         0x4005a9

## 치팅 (자료 확인 해본 영역)
    1.ROPgadget --binary ./basic_rop_x64 --re ""
        가젯 찾기 명령어

    2.payload += pop_rdi
    payload += p64(1)
    payload += pop_rsi
    payload += p64(read_got)    #plt는 got참조하여 실행하니 got주소 알아야함
    payload += p64(0)
    payload += p64(write_plt)   #read_got 출력시키기
        read_got주소 출력시키기
    

## Vulnerability Root Cause
- read() 호출 시 입력 길이 검증 부재
- Stack Buffer Overflow 발생

## Exploitation Summary
- Rop 기반 ret2libc 공격
- GOT leak -> libc base 계산 -> system("/bin/sh")

## Secure Coding / Mitigation
- read -> fgets/    read size 제한
- Stack Canary 활성화
- PIE + RELRO 적용 
    ㄴ gadget 주소 매번 변경 + GOT 보호(런타임 이후 GOT를 읽기 전용으로 변경)
