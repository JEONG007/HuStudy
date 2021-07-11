# 우선순위 큐 구현
# heapq 이용, 숫자가 작을수록 우선순위 높음
# HINT : heapq.heappush(), heapq.heappop()

import heapq

t = int(input())
for i in range(t):
    n = int(input())
    hq = []
    for j in range(n):
        q = int(input())
        if q == -1:
            if len(hq) != 0:
                print(heapq.heappop(hq))
        else:
            heapq.heappush(hq,q)