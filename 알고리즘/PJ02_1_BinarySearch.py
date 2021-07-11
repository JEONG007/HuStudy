#이진탐색
#정렬된 리스트와 찾고자 하는 숫자 리스트가 입력되었을 때,
#리스트에서 찾고자 하는 숫자와 차이가 가장 작은 값을 출력

def binary2(l, x):
    #x가 첫번째 값보다 작거나 마지막 값보다 큰 경우를 미리 확인
    if x <= l[0]: return l[0]
    if x >= l[-1]: return l[-1]
    
    start = 0
    end = len(l)
    
    while start < end:
        index = (start + end)//2 #중간 위치로 인덱스 조정
        #찾은 경우를 빼야할 수도 있음
        if x == l[index]: #찾음!
            return l[index]
        elif x < l[index]: # 중간 인덱스 왼쪽에 존재
            end = index
        else: # 중간 인덱스 오른쪽에 존재
            start = index + 1
    #위에서 return이 없었다면 l[end-1] < x < l[end]가 항상 성립
    #두 값중 x와 더 가까운 값 반환
    if abs(l[end-1] -x) <= abs(l[end]-x): return l[end-1]
    else: return l[end]
    
t = int(input())
for _ in range(t):
    l = list(map(int, input().split()))
    q = list(map(int, input().split()))
    ans = [binary2(l,x) for x in q]
    print(*ans)