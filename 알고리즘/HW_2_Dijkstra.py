#최단 경로 구하기
#모든 가중치가 양수인 방향성 그래프가 주어졌을 때, 
#두 점 사이의 최단 경로를 구하는 알고리즘

import heapq

T = int(input())    
for i in range(T):  
    INF = int(1e9)
    N,M = map(int,input().split())
    graph=[[] for _ in range(N+1)]
    distance_arr = [INF] * (N+1)
    for j in range(M):
        u,v,c = map(int,input().split())
        graph[u].append((c,v)) 
        
    
    distance_arr[0] = 0

    hp = []
    heapq.heappush(hp,(0,0))
    while hp:
        dist, cur = heapq.heappop(hp)
        if distance_arr[cur] < dist:
            continue
        for j in graph[cur]:
            cost = dist + j[0]
            next = j[1]
            if distance_arr[next] > cost :
                distance_arr[next] = cost
                heapq.heappush(hp,(cost,next))
    if distance_arr[N-1] == INF:
        print(-1)
    else:
        print(distance_arr[N-1])