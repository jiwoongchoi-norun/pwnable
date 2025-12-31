## 프로그램 흐름
커널에서 main함수를 호출하면서 push rip 그리고  main함수 프롤로그에서 push rbp를 진행하여 스택에 먼저 넣는다 -> leave rbp pop rip
지역변수를 할당하고 초기화 함수 실행 **gets**로 입력받고 프로그램이 종료된다

## 보호기법
    elf 32비트
    no canary   -> 스택보호 난수 없음
    nx enable   -> 스택,힙 메모리 실행 불가
    no pie      -> 바이너리 기준 주소 고정

## 스택구조
    rip(return address) 4bytes
    rbp(saved rbp)      4bytes
    지역변수
    buf                 128bytes

## 취약점
    gets(buf)
        -> 입력길이가 제한없는 취약점이 있다
    read_flag()
        -> 바이너리 기준 주소가 고정이기에 함수 주소 획득 가능
        -> 0x080485b9  read_flag 주소 확인

## 시나리오
    buf변수에 패딩값으로 스택을 채우고 rip 4바이트에 read_flag()함수 주소를 리틀엔디안 값으로 채우면 프로그램이 종료될때 복귀하는 함수를 조작하여 원하는 값(flag) 얻을수 있을 것 이다.

## 패치
    gets(buf) -> gets_s(buf,sizeof(buf))
              -> fgets(buf,sizeof(buf),stdin)

## 배운점
