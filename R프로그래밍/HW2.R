setwd("C:/Users/Jeong/Documents/Hustar_Study/Rcode/Day2/")
getwd()

library(dplyr)
library(ggplot2)

#1
sat2010 = read.csv("SAT_2010.csv")

#1-A
#“write”와 “math”에 대해 boxplot과 histogram을 그려라. 
#그린 그래프를 통해 각각의 분포를 설명하고 비교하라.  
attach(sat2010)
par(mfrow=c(1,1))
boxplot(write,math)
par(mfrow=c(1,2))
hist(write, col="lightblue")
hist(math, col="lightblue")

#1-B
#산점도를 그려보고 
#“total” 변수와 가장 의미 있다고 생각하는 변수를 제시하고 설명해라 
par(mfrow=c(1,1))
plot(expenditure, total)
plot(pupil_teacher_ratio, total)
plot(salary, total)
plot(read, total)
plot(math, total)
plot(write, total)
plot(sat_pct, total)

#1-C
#B에서 선택한 변수와 total 변수 간의 산점도를 그리고 
#이를 바탕으로 최적적합함수를 추정하여 그래프로 그려라. (선형, 비선형) 
par(mfrow=c(1,1))
plot(read, total)
abline(lm(total~read), col="red")
lines(lowess(read,total), col="blue")
detach(sat2010)


#2
sch = read.csv("search.csv")
sch_gender = read.csv("search_gender.csv")
sch_age = read.csv("search_age.csv")
sch_local = read.csv("search_local.csv")

#2-A
#search.csv를 data로 읽었다 하자. data$일 = as.Date(data$일) 을 적용하라.
sch$일 = as.Date(sch$일)

#2-B
#검색량.csv 데이터를 geom_line을 통해 다음과 같이 표현후, 
#일자별 검색량 변화를 설명하라.
par(mfrow=c(1,1))
ggplot(sch, mapping=aes(x=일,y=검색량))+ 
  geom_line(aes(x=일,y=BTS, colour="bts"))+
  geom_line(aes(x=일,y=zoom, colour="zoom")) +
  geom_line(aes(x=일,y=라면, colour="라면")) +
  geom_line(aes(x=일,y=코로나, colour="코로나"))

#2-C
#검색량_성별.csv데이터를 다음과 같이 bar chart로 표현하고, 
#성별 및 품목별 검색량 차이를 비교하라. 
par(mfrow=c(1,2))

ggplot(sch_gender,mapping = aes(품목, count, fill=성별))+
  geom_bar(stat = "identity")

ggplot(sch_gender,mapping = aes(성별, count, fill=품목))+
  geom_bar(stat = "identity", position = "dodge")
  
#2-D
#검색량_연령.csv데이터를 다음과 같이 scatter Plot으로 표현해라
par(mfrow=c(1,1))

ggplot(sch_age, mapping=aes(x=연령,y=count))+ 
  geom_point(aes(x=연령,y=BTS, colour="bts"))+
  geom_point(aes(x=연령,y=zoom, colour="zoom")) +
  geom_point(aes(x=연령,y=라면, colour="라면")) +
  geom_point(aes(x=연령,y=코로나, colour="코로나"))

#2-E
#검색량_지역.csv데이터를 다음과 같이 Histogram으로 표현해라.
ggplot(sch_local, mapping=aes(x=지역, fill=검색어))+
  geom_histogram(stat="count")

