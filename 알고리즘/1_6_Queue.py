# 큐 구현하기
# collections 사용

import collections

t = int(input())
for i in range(t):
    n = int(input())
    queue = collections.deque([])
    for j in range(n):
        q = int(input())
        if q == -1:
            if len(queue) != 0:
                print(queue.popleft())
        else:
            queue.append(q)