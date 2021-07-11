# 세금 징수
# 특정 금액이 주어졌을 때, 해당 금액을 만드는 동전(지폐)의 최소 개수를 구함
# Greedy
t = int(input())
            
for _ in range(t):
    n = int(input())
    coins = [50000, 10000, 5000, 1000, 500, 100]
    c_sum = 0
    for i in coins:
        c_sum += n // i
        n %= i
        
    print(c_sum)