# 스택 구현하기
# Hint : list의 pop() 함수 사용

t = int(input())
for i in range(t):
    n = int(input())
    mList = list()
    for j in range(n):
        q = int(input())
        if q == -1:
            if len(mList) != 0:
                print(mList.pop())
        else:
            mList.append(q)