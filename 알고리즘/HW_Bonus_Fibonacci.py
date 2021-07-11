#피보나치 수열
#첫째 항과 둘째 항이 1
#셋째 항 부터는 Fn=Fn−1+Fn−2 공식에 따라 만들어짐
#n이 주어졌을 때, 피보나치 수열의 n번째 항을 출력

t = int(input())

for _ in range(t):
    n = int(input())
    Fibo = [0] * (n+1)
    
    if n >= 0:
        Fibo[0] = 0
    if n >= 1:
        Fibo[1] = 1
    
    if n >= 2:
        for i in range(2, n+1):
            Fibo[i] = Fibo[i-1] + Fibo[i-2]
    
    print(Fibo[n])