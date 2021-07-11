#DFS
#무방향 그래프가 주어졌을 때, 정점 0부터 시작하여 
#그래프를 깊이우선탐색(DFS)으로 순회하는 알고리즘
#여러 선택지 존재 시 번호가 가장 낮은 정점을 우선적으로 선택

import sys
sys.setrecursionlimit(1000000)

def DFS(v, List, Check):
    Check.append(v)
    print(v, end = " ")
        
    for i in List[v]:
            if i not in check:
                DFS(i, List, Check)
#                 bfs.append(i)
#                 print("update : ", bfs)
    

t = int(input())
for _ in range(t):
    N, M = map(int, input().split())
    List = [[] for _ in range(N)]
    for i in range(M):
        u, v = map(int, input().split())
        List[u].append(v)
        List[v].append(u)
    for i in range(N):
        List[i].sort()
        
    check = []
    DFS(0, List, check)
    
    print()