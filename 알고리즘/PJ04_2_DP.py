#세계 암기 대회
#n x m 좌표 평면과 평면의 점수판이 주어질 때 잃는 최소의 점수
#점수가 있는 셀을 밟으면 해당 셀의 점수를 잃음
#이동은 오른쪽, 아래쪽, 혹은 오른쪽 아래 대각선만 가능

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
                UT[i][j] = T[i][j] + min(UT[i][j-1],UT[i-1][j], UT[i-1][j-1])
                
    #(0,0)에서 (i,j)에 도달했을 때 얻을 수 있는 최대 점수
    print(UT[n-1][m-1]) 