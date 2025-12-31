## 문제 요약
- scanf("%141s", buf); 
    ㄴ buf의 사이즈가 128바이트인데 141바이트까지 입력이 가능하니 rip변조 가능 

## 프로그램 흐름
     커널에서 elf헤더 파싱 메모리 매핑
     _start
     _libc_start_maind  main호출
     call main -> push rip(return address)
     main 함수 프롤로그 
        push rbp (saved rbp)
        mov rbp,rsp
        sub rsp,0x30 ->지역변수 공간
    leave
        mov rsp,rbp
        pop rbp
    ret
        pop rip 이전 함수 복귀
    
## 보호 기법
    32비트 
    no canary
    nx unknown
    no pie
## 스택 구조
    rip         4바이트
    saved rbp   4바이트
    buf         128바이트

## 취약점
-   char buf[0x80];     --- 128바이트 크기
    scanf("%141s", buf); --- 141바이트 크기
ㄴ 128 + 4 + 4
    ㄴ 변수에 쉘코드 + 패딩 + 변수 주소(rip)

## 시나리오
- buf변수에 4바이트 쉘코드값이 있고 패딩으로 채우고 rip에 buf변수 주소를 채운다
- scanf로 입력을 받으니 변수에 쉘코드를 00 0a 20 탭이 없는 쉘코드를 사용해야 하니 **shellcraft()**가 아닌 검증된 코드를 사용해야한다


## 패치
- scanf("%127s",buf)
    ㄴ bof방지
- fgets(buf,sizeof(buf),stdin);
    ㄴ 길이 자동 제한, 안전

## 배운 점
- 
nx unknown
ㄴ NX는 스택/힙 데이터 영
scnaf
ㄴ  \x00 문자열 종료
    \x0a \n입력 종료
    \x20 공백   
이것이 없는 검증된 쉘코드를 사용해야함
    ㄴshellcraft()불가