# 두 바퀴 레이스
# 첫 번째 바퀴를 완주한 순서와 두 번째 바퀴를 완주한 순서가 같은지 체크
# 하나의 숫자는 반드시 두 번만 나타남
# HINT : 큐를 이용
# 순위가 바뀌었다면 YES를, 아닌 경우에 NO를 각 줄에 출력

import collections

def Race():
    queue = collections.deque([])
    
    car = list(map(int, input().split()))
    
    for i in car:
        if i in queue:
            if queue.popleft() != i:
                return "YES"
        else:
            queue.append(i)
            
    if not len(queue):
        return "NO"

t = int(input())
            
for _ in range(t):
    print(Race())