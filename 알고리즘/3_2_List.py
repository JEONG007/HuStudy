# 인접 리스트 구현하기
# 가중치가 없는 무방향성 그래프가 주어졌을 때 이를 인접 리스트로 표현
# 간선(u,v) : u에서 v로 가는 간선

t = int(input())

for _ in range(t):
    N, M = map(int, input().split()) #정점의 개수, 간선의 개수
    List = [[] for _ in range(N)]
    
    for _ in range(M):
        u, v = map(int, input().split()) #u에서 v로 가는 간선
        List[u].append(v)
        List[v].append(u)
        
    
    for i in range(N):
        List[i].sort()
        print(*List[i])