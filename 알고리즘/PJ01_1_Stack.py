# 괄호가 올바른 괄호열인지 체크하는 프로그램
# 올바른 예 : ((){}[[]])

t = int(input())

def Compare(my_str):
    my_list = list()
    for i in my_str:
        if i == '(' or i == '{' or i == '[':
            my_list.append(i)
        elif i == ')':
            if not len(my_list):
                return 0
            if my_list.pop() != '(':
                return 0
        elif i == '}':
            if not len(my_list):
                return 0
            if my_list.pop() != '{':
                return 0
        elif i == ']':
            if not len(my_list):
                return 0
            if my_list.pop() != '[':
                return 0
    if len(my_list):
        return 0
    else:
        return 1

for _ in range(t):
    my_str = input()
    if Compare(my_str):
        print("YES")
    else:
        print("NO")