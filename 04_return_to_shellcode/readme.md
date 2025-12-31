## 프로그램 흐름
커널 -> main 프롤로그 =>rip rbp push
buf는 0x50바이트 크기
buf의 주소,buf와 rbp사이 거리 알려준다
buf 0x100바이트크기로 입력 받고 출력시킴
buf 0x30입력 받고 종료

## 보호 기법
    아키텍처 amd64
    canary found
    nx unknown
    pie enabled

## 스택구조
rip 8바이트
rbp 8바이트
canary 8바이트  rbp - 0x08
buf 0x50바이트  rbp - 0x60

## 취약점
1. buf주소를 알려준다 == rbp -0x60,계속 변화
2. rbp와 rbp-0x60 거리 알려준다 == 10진수 96출력
3. 0x100 입력 받는다
4. buf 출력한다 **canary 유출**
    ㄴ 96칸에서 1~8칸 카나리 9~96
5. buf입력 받고 종료 
    ㄴ 카나리 포함 bof payload 공격

## 시나리오
첫입력일때 카나리 앞까지 입력하고 출력될때 카나리 유출하고 그 값을 저장해서 두번떄 입력시에 카나리 값 그리고 쉘코드 buf주소까지 스택을 조작하여 공격

## 배운점
1. sh=asm(shellcraft.sh())
    쉘코드 어셈블리 문자열을 바이트 기계어로 변환
2. canary 첫 바이트 = \x00
3. 카나리 출력 저장할때 리틀엔디안으로 출력됨
4. buf_addr = int(p.recvline().strip(),16)
    저장시에 앞,뒤 개행문자 탭 등 제거 후 16진수 정수값으로 저장
5. p64()는 정수형 -> 바이트 u64()는 바이트를 정수형으로
6. recvuntil after 등 문자열 b'' 표시 필수
7. recvuntil() 단순 변수값 지정 가능
8. payload_2nd = sh.ljust(88,b'a') sh를 맨 앞 그리고 뒤를 88크기만큼 패딩

## 성공 로그
1. buf 주소 저장
2. rbp 거리 저장 + 카나리 유출
