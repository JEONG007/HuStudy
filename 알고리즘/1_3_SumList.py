#테스트 케이스만큼 리스트를 입력 받고, 그 리스트의 합을 출력

#1 : 직접 구현
t = input()
for i in range(int(t)):
    mlist = input().split()
    msum = 0
    for j in range(len(mlist)):
        msum += int(mlist[j])
    print(msum)

#2 : 내장함수 이용
t = input()
for i in range(int(t)):
    mlist = list(map(int, input().split()))
    print(sum(mlist))