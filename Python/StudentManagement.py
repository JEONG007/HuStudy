import sys

#ReadFile 데이터 불러오기
def ReadFile(dic):
    #파일 오픈
    if len(sys.argv) == 1:
        fr = open("students.txt", "r")
    else:
        fr = open(sys.argv[1], "r")
    
    
    for line in fr:
        stu = line.replace("\n","")
        stu = stu.split("\t")
        
        stu.append(Average(stu[2:])) #평균 계산
        stu.append(Grade(stu[4])) #학점 계산
        
        dic[stu[0]] = stu[1:]
        
    fr.close()
     
def Average(stu): #평균
    return (int(stu[0]) + int(stu[1]))/2

def Grade(avg): #학점
    if avg >= 90:
        return 'A'
    elif 90 > avg >= 80:
        return 'B'
    elif 80 > avg >= 70:
        return 'C'
    elif 70 > avg >= 60:
        return 'D'
    else :
        return 'F'
        

#show 전체 학생 정보 출력
def show(dic):
    print("%10s %15s %9s %8s %10s %8s" %('Student', 'Name', 'Midterm', 'Final', 'Average', 'Grade'))
    
    #x에 학생 한명의 리스트가 순차적으로 들어감
    stus = sorted(dic.items(), key= lambda x:x[1][3], reverse=True) #sort
    print(" ----------------------------------------------------------------")
    for i in stus:
        print("%10s %15s %7s %9s %10.1f %7s" %(i[0], i[1][0], i[1][1], i[1][2], i[1][3], i[1][4]))
    print()

#search 특정 학생 검색
def search(dic):
    s_id = input("Student ID: ")
    
    if s_id not in dic: # 학생 없음
        print("NO SUCH PERSON.\n")
    else: #학생 있음
        print("%10s %15s %9s %8s %10s %8s" %('Student', 'Name', 'Midterm', 'Final', 'Average', 'Grade'))
        print(" ----------------------------------------------------------------")
        print("%10s %15s %7s %9s %10.1f %7s" %(s_id, dic[s_id][0], dic[s_id][1], dic[s_id][2], dic[s_id][3], dic[s_id][4]))
        print()
    
#changescore 점수 수정
def changescore(dic):
    s_id = input("Student ID: ")
    
    if s_id not in dic: # 학생 없음
        print("NO SUCH PERSON.\n")
    else:
        bef = dic[s_id][:]
        
        #값 입력
        select = input("Mid/Final? ").lower()
        if select == "mid":
            score = input("Input new score: ")
            if 0<= int(score) <= 100:
                dic[s_id][1] = score
            else:
                print("올바른 값이 아닙니다.\n")
                return
                
        elif select == "final":
            score = input("Input new score: ")
            if 0<= int(score) <= 100:
                dic[s_id][2] = score
            else:
                print("올바른 값이 아닙니다.\n")
                return
        else:
            print("취소\n")
            return
        
        #출력
        dic[s_id][3] = Average(dic[s_id][1:3])
        dic[s_id][4] = Grade(dic[s_id][3])
        print("%10s %15s %9s %8s %10s %8s" %('Student', 'Name', 'Midterm', 'Final', 'Average', 'Grade'))
        print(" ----------------------------------------------------------------")
        print("%10s %15s %7s %9s %10.1f %7s" %(s_id, bef[0], bef[1], bef[2], bef[3], bef[4]))
        print("Score changed.")
        print("%10s %15s %7s %9s %10.1f %7s\n" %(s_id, dic[s_id][0], dic[s_id][1], dic[s_id][2], dic[s_id][3], dic[s_id][4]))
        

#add 학생 추가
def add(dic):
    s_id = input("Student ID: ")
    if s_id in dic:
        print("ALREADY EXISTS.\n")
    else:
        #정보 입력
        name = input("Name: ")
        mid = input("Midterm Score: ")
        if not 0<= int(mid) <= 100:
            print("올바른 값이 아닙니다.\n")
            return
        fin = input("Final Score: ")
        if not 0<= int(fin) <= 100:
            print("올바른 값이 아닙니다.\n")
            return
        print("Student added.\n")
        
        #딕셔너리에 추가
        dic[s_id] = [name, mid, fin]
        dic[s_id].append(Average(dic[s_id][1:3]))
        dic[s_id].append(Grade(dic[s_id][3]))

#searchgrade 학점 검색
def searchgrade(dic):
    grade = input("Grade to search: ").upper()
    if ('A' <= grade <= 'F') and (grade != 'E'):
        stus = list()
        #학년 검색 후 stus에 추가
        for s_id in dic:
             if dic[s_id][4] == grade:
                    stus.append([s_id,dic[s_id][3]])
        if len(stus) == 0:
            print("NO RESULTS.\n")
        else:
            print("%10s %15s %9s %8s %10s %8s" %('Student', 'Name', 'Midterm', 'Final', 'Average', 'Grade'))
            print(" ----------------------------------------------------------------")
            stus = sorted(stus, key= lambda x:x[1], reverse=True) #sort
            for (s_id, avg) in stus:
                print("%10s %15s %7s %9s %10.1f %7s" %(s_id, dic[s_id][0], dic[s_id][1], dic[s_id][2], dic[s_id][3], dic[s_id][4]))
            print()
    else:
        print("올바른 값이 아닙니다.\n")

#remove 특정 학생 삭제
def remove(dic):
    if len(dic) == 0:
        print("List is empty.\n")
        return
        
    s_id = input("Student ID: ")
    if s_id not in dic:
        print("NO SUCH PERSON.\n")
    else:
        del dic[s_id]
        print("Student removed.\n")

#quit 데이터 저장 및 종료
def quit(dic):
    save = input("Save data?[yes/no] ").lower()
    
    if save == "yes":
        name = input("File name: ")
        fw = open(name, "w")
        
        stus = sorted(dic.items(), key= lambda x:x[1][3], reverse=True) #sort
        for s_id, s_val in stus:
            stu = "%s\t%s\t%s\t%s\n" %(s_id, s_val[0], s_val[1], s_val[2])
            fw.write(stu)
        
        fw.close()

#실행은 여기!!
dic = {}

ReadFile(dic)
show(dic)

while True:
    choice = input("#").lower()
    
    if choice == "show":
        show(dic)
    elif choice == "search":
        search(dic)
    elif choice == "changescore":
        changescore(dic)
    elif choice == "add":
        add(dic)
    elif choice == "searchgrade":
        searchgrade(dic)
    elif choice == "remove":
        remove(dic)
    elif choice == "quit":
        quit(dic)
        break
    else:
        print()
