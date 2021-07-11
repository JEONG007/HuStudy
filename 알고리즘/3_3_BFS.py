#BFS
#방향성 그래프가 주어졌을 때, 정점 0부터 시작하여 
#그래프를 너비우선탐색(BFS)으로 순회하는 알고리즘을 작성

from collections import deque

t = int(input())
for _ in range(t):
    N,M = map(int, input().split())
    List = [[] for _ in range(N)]
    
    for i in range(M):
        u, v = map(int, input().split())
        List[u].append(v)
        
    for i in range(N):
        List[i].sort()
#         print(*List)
#         print(*List[i])######

    bfs = deque([])
    check = [] #방문한 노드 저장
    bfs.append(0)
    
    while bfs:
        q = bfs.popleft()
        check.append(q)
        print(q, end = " ")
#         print("bfs : ", bfs)
#         print("check : ", check)
        for i in List[q]:
            if i not in bfs and i not in check:
                bfs.append(i)
#                 print("update : ", bfs)
        
    print()