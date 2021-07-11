#무거운 용액
#각 용액의 총 질량과 부피가 주어졌을 때 
#용액들을 합성하여 주어진 부피의 최대 무게를 계산

def cmp(x): #부피 당 질량을 반환
    return x[0]/x[1]

T = int(input())
for _ in range(T):
    #C는 만들어야할 용액의 부피이자, 남은 부피라고 생각
    N, C = map(int, input().split()) 
    liquidlist = []
    for i in range(N):
        liquidlist.append(tuple(map(int,input().split())))
        
    #부피 당 질량이 큰 순서로 내림차순 정렬
    liquidlist.sort(key = cmp, reverse = True) 
    maxg = 0 # 이 문제의 답
    
    for i in range(N): #부피 당 질량이 큰 순서대로
        if C >= liquidlist[i][1]:#만약 다 넣을 수 있다면
            maxg += liquidlist[i][0] #다 넣었을 때의 질량을 더하고
            C -= liquidlist[i][1]    #그 만큼 부피를 뺸게 남았다
        else: #다 넣을 수 없다면
            maxg += (C * cmp(liquidlist[i])) #C 정도만 넣는다.
            break #다 넣었으니까 break
    print(int(maxg)) #소수점 버리기