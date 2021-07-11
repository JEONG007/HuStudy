# 돌다리 건너기(DP,Dynamic Programming)
# 돌다리의 개수 n이 주어질 때, n번째 돌다리까지 도달할 수 있는 방법의 수
# T[i] : i번 돌다리에 도달하는 경우의 수 % 1904101441
# 재귀 식(점화 식) : T[i] = (T[i-1] + T[i-2] + T[i-3]) % 1904101441
# 기저 조건(초기 값) : i = 1일 때, T[i] = 1, i = 2일 때, T[i] = 2, i = 3일 때, T[3] = 1

#1
t = int(input())

for _ in range(t):
    n = int(input())
    T = [0] * (n+1)
    
    for i in range(1, n+1):
        if i == 1:
            T[i] = 1
        elif i == 2:
            T[i] = 2
        elif i == 3:
            T[i] = 4
        else:
            T[i] = (T[i-1] + T[i-2] + T[i-3]) % 1904101441
    print(T[n])

#2
t = int(input())

for _ in range(t):
    n = int(input())
    T = [0] * (n+1)
    
    if n >= 1:
        T[1] = 1
    if n >= 2:
        T[2] = 2
    if n >= 3:
        T[3] = 4
        
    if n>3:
        for i in range(4, n+1):
            T[i] = (T[i-1] + T[i-2] + T[i-3]) % 1904101441
        
    print(T[n])