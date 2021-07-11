#최대값과 최솟값의 차이

t = int(input())
for i in range(t):
    mList = list(map(int,input().split()))
    mMax = max(mList)
    mMin = min(mList)
    print(mMax-mMin)




