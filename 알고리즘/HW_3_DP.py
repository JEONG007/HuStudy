#더블로 가
#1번 ~ n번 발판에 적힌 점수가 차례대로 주어졌을 때, 
#게임이 끝나고 얻을 수 있는 점수의 최대값을 출력하는 프로그램
#규칙1 : 인접한 발판으로만 이동하거나 혹은 한 칸을 점프해서 그 다음 칸으로 갈 수 있음
#규칙2 : 현재 밟고 있는 발판이 k번 발판이라면 바로 2k번 발판으로 점프하는 더블 이동 가능

def dbro(l, n):
    DP = [0]*len(l)
    for i in range(1, n+1):
        if i == 1: #초기조건: 시작발판
            DP[i] = l[i]
        elif i % 2 == 1: #홀수 발판
            DP[i] = max(DP[i-1], DP[i-2]) + l[i]
        else: #짝수 발판
            DP[i] = max(DP[i-1], DP[i-2], DP[i//2]) + l[i]
    return DP[n]

testnum = int(input())
for _ in range(testnum):
    n = int(input())
    lis = list(map(int, input().split()))
    lis = [0] + lis #문제와 index를 맞추기 위함
    print(dbro(lis, n))