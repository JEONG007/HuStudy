setwd("C:/Users/Jeong/Documents/Hustar_Study/Rcode/Day1_hw1/")
getwd()
install.packages("dplyr")
library(dplyr)


#1
autompg<-read.csv("autompg.csv")

#1-A
#autompg data에서 실린더(cyl)가 8인 데이터만 추출하고 horsepower의 평균을 구하여라. 
#실린더(cyl)이 4인 데이터를 추출하여 평균을 구하고 비교하라.
A1 <- subset(autompg, cyl==8)
attach(A1)
mean(hp)
detach(A1)

A2 <- subset(autompg, cyl==4)
attach(A2)
mean(hp)
detach(A2)

#1-B
#autompg data에서 carname에 ‘chevrolet’이 들어간 차량의 데이터를 추출하라. 
#몇 개의 데이터가 존재하나? 
attach(autompg)
B = subset(autompg, grepl('chevrolet', carname) == TRUE)
detach(autompg)
dim(B)

#2
hitters = read.csv("Hitters.csv")

#2-A
#각 선수별 타율을 계산하여 기존 테이블에 넣어라
#타율 =- Hits/AtBat
attach(hitters)
hitters['BatAvg'] = Hits/AtBat
#hitters = hitters %>% mutate(BatAvg = Hits/AtBat)

#2-B
#각 선수별 출루율을 계산하여 기존 테이블에 넣어라.
#출루율 = (Hits + Walks)/(AtBat + Walks)
hitters['OBP'] = (Hits + Walks)/(AtBat + Walks)
detach(hitters)

#2-C
#타율과 출루율의 평균, 중앙값을 계산하라.
attach(hitters)
BatAvg_mean = mean(BatAvg)
BatAvg_median = median(BatAvg)
OBP_mean = mean(OBP)
OBP_median = median(OBP)
detach(hitters)

#2-D
#출루율과 타율이 모두 평균보다 높거나 같은 선수는 전체에서 몇 퍼센트의 비율을 차지하는가?
attach(hitters)
set1 = subset(hitters, BatAvg >= BatAvg_mean, OBP>= OBP_mean)
nrow(set1)/nrow(hitters)
detach(hitters)

#2-E
#기존 Data에서 CAtBat CHits CHmRun CRuns CRBI CWalks만 선택하여 새로운 데이터를 만들어라.
attach(hitters)
hitSet = select(hitters, CAtBat, CHits, CHmRun, CRuns, CRBI, CWalks)
head(hitSet)
detach(hitters)

#2-F
#E의 결과에 대해 mean, min, max와 min과 max의 차이를 보여주는 표를 만들어라.
mm = function(n){
  return( max(n) - min(n) )
}

# table with descriptive statistics
a1 <- hitSet %>% summarize_all(mean)
a2 <- hitSet %>% summarize_all(min)
a3 <- hitSet %>% summarize_all(max)
a4 <- hitSet %>% summarize_all(mm)
table1 <- rbind(a1,a2,a3,a4)
rownames(table1) <- c("mean","min","max","max-min")
tablet<-t(table1)
tablet
