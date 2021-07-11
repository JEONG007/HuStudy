#이진 탐색
#반복문(종료조건)을 돌리면서 중간 인덱스를 찾고,
#중간 인덱스에 위치한 값을 이용해 절반을 제거하는 방식

t = int(input()) 

for _ in range(t):
    data = list(map(int, input().split()))
    query = list(map(int, input().split()))
    answer = []
    
    for q in query:
        left = 0
        right = len(data) - 1
        
        while left <= right:
            index = (left + right)//2 #중간 위치로 인덱스 조정
            if q == data[index]: #찾음!
                answer.append(index)
                break
            elif q < data[index]: # 중간 인덱스 왼쪽에 존재
                right = index - 1
            else: # 중간 인덱스 오른쪽에 존재
                left = index + 1
                
        if left > right: #찾는 값이 존재하지 않음
            answer.append(-1)
    print(*answer)   