# 인접 행렬 구현하기
# 가중치가 있는 방향성 그래프가 주어졌을 때 이를 인접 행렬로 표현
# 간선(u,v,c) : u에서 v로 가는 비용이 c인 간선
# 간선이 존재하지 않는다면 0을 출력

t = int(input())

for _ in range(t):
    N, M = map(int, input().split()) #정점의 개수, 간선의 개수
    Matrix = [[0]*N for _ in range(N)]
    
    for _ in range(M):
        u, v, c = map(int, input().split()) #u에서 v로 가는 비용이 c인 간선
        Matrix[u][v] = c
    
    for i in range(N):
        # for j in range(N):
        #     print(Matrix[i][j], end = ' ')
        print(*Matrix[i])