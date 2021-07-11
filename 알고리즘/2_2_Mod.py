# n^k mod m 효율적으로 계산하기
# HINT1 : 𝒂b % 𝒙 = ((𝒂 % 𝒙) ∗ (𝒃 % 𝒙)) % x
# HINT2 : x^a*x^b = x^(a+b)
# HINT3 : k가 홀수일 때와 짝수일 때?
t = int(input())

def Power(n, k, m):
    if k == 0:
        return 1
    if k == 1:
        return n
        
    power = Power(n, k//2, m)
    
    if k % 2 == 0:
        return (power * power) % m
    else:
        return (power * power * n) % m

for _ in range(t):
    n, k, m = map(int, input().split())
    print(Power(n, k, m))