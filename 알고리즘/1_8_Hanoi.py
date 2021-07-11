# 하노이 탑
# 3개의 기둥 A,B,C가 있고, A에 있는 n개의 무게가 다른 원판을 C로 옮기고자 함
# 규칙1 : 원판은 한 번에 한 개씩 제일 위에 있는 원판만 이동 가능
# 규칙2 : 원판은 항상 무거운 것이 아래에 있어야 함
# A에서 C로 최소 횟수로 이동. 이를 출력
# HINT : 재귀 함수 이용

def Hanoi(n, start, mid, end):
    if n == 0:
        return
    Hanoi(n-1, start, end, mid)
    print(start, "->", end)
    Hanoi(n-1, mid, start, end)

T = int(input())
for _ in range(T):
    n = int(input())
    Hanoi(n, 'A', 'B', 'C')