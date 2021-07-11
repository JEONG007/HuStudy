#합병
#입력된 두 리스트의 모든 값을 합병하여 오름차순으로 정렬 후
#각 원소는 어떤 리스트에서 가져온 값인지 출력

from collections import deque

t = int(input())

for _ in range(t):
    List1 = deque(list(map(int, input().split())))
    List2 = deque(list(map(int, input().split())))
    
    while True:
        if (not len(List1)) and (not len(List2)):
            break # 두 리스트에 원소 없음
        elif not len(List1): #리스트1에 원소 없음
            List2.popleft()
            print(2, end = ' ')
        elif not len(List2):#리스트2에 원소 없음
            List1.popleft()
            print(1,end = ' ')
        else:#두 리스트에 원소 있음
            if List1[0] <= List2[0]:
                List1.popleft()
                print(1,end = ' ')
            else:
                List2.popleft()
                print(2,end = ' ')