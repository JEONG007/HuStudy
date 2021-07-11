#암기대회
#오른쪽, 아래쪽으로 가면서 얻을 수 있는 가장 높은 점수를 계산
t = int(input())

for _ in range(t):
    n, m = map(int, input().split())
    
    T = []
    for _ in range(n):
        T.append(list(map(int, input().split())))
        
    UT = [[0]*m for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0: #시작 칸인 경우
                UT[i][j] = T[i][j]
            elif i == 0: #제일 위쪽 줄인 경우 왼쪽에서밖에 올 수 없다.
                UT[i][j] = UT[i][j-1] + T[i][j]
            elif j == 0:#제일 왼쪽 줄인 경우 위쪽에서밖에 올 수 없다.
                UT[i][j] = UT[i-1][j] + T[i][j]
            else: #그 외의 경우
                UT[i][j] = max(UT[i][j-1],UT[i-1][j]) + T[i][j]
                
    #(0,0)에서 (i,j)에 도달했을 때 얻을 수 있는 최대 점수
    print(UT[n-1][m-1]) 