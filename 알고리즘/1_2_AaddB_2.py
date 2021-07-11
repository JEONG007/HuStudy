#테스트 케이스만큼 입력 받아, 각각의 합을 출력

t = int(input()) #테스트 케이스 개수
for i in range(t):
    a, b = map(int, input().split())
    print(a+b)