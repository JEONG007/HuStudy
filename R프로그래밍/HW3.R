setwd("C:/Users/Jeong/Documents/Hustar_Study/Rcode/Day3/")
getwd()

library(dplyr)
library(ggplot2)

#1
M40 = read.csv("NSC2_M40_1000.csv")#환자의 상병내역을 기록한 표
BNC = read.csv("NSC2_BNC_1000.csv")#건강보험 자격 및 보험료 표

#1-step1
#NSC2_M40_1000.csv 에서 2002년부터 2008년까지의 연도별 환자의 방문횟수를 계산한다.
#방문횟수를 number라는 변수로 만들어 RN_INDI, STD_YYYY, number를 
#column으로 가지는 새로운 table을 만들어라.
newM40 = subset(M40,M40$STD_YYYY <= 2008)
step1 = newM40 %>% group_by(RN_INDI,STD_YYYY) %>% summarise(number = n())
table1 <- rbind(step1)
table1

#1-step2
#NSC2_BNC_1000.csv와 Step1을 STD_YYYY, RN_INDI를 key로 하여 inner join한다.
step2 = inner_join(step1, BNC, by = c("STD_YYYY", "RN_INDI"))

#1-step3
#가장 환자의 방문횟수가 높은 환자의 ID와 해당 연도를 적으시오 
arrange(step2, desc(step2$number))


#2
sat2010 = read.csv("SAT_2010.csv") #U.S SAT scores by state for 2010

#2-A
#Total 변수의 분산과 평균값은? 중앙값은? 
attach(sat2010)
mean(total) #평균
var(total) #분산
median(total) #중앙값

#2-B
#Total 변수가 (평균 ??? 표준편차, 평균 + 표준편차) 
#즉, 1시그마 범위 내에 속하는 state의 수는 ?
subset(sat2010, total <= mean(total)+sd(total) &
         total >= mean(total) - sd(total)) %>% summarise(n())

#2-C
#Total의 평균으로부터 가장 멀리 떨어진 Total값을 가진 state의 이름은 무엇인가? 
Csat2010 = select(sat2010, state, total)
Csat2010$total = abs(total-mean(total))
head(arrange(Csat2010, desc(Csat2010$total)))

#2-D
#ggplot을 이용하여 Salary가 50000이상인 데이터와 
#이하인 데이터에 대해 Sat_pct와 total 을 이용해 Plot graph를 그리시오.
par(mfrow=c(1,1))
D1 = subset(sat2010, salary >= 50000)
D2 = subset(sat2010, salary < 50000)
ggplot(D1, mapping=aes(x=sat_pct,y=total))+ geom_point()
ggplot(D2, mapping=aes(x=sat_pct,y=total))+ geom_point()
  
#2-E
#정규확률도를 그리고, Shapiro-Wilks test도 하여 비교평가
qqnorm(total)
qqline(total)
shapiro.test(total)

detach(sat2010)

#3
piz = read.csv("pizzar.csv") #피자배달 데이터

#3-1
#상자그림(boxplot)을 그리고 비교설명
attach(piz)
par(mfrow=c(1,1))
boxplot(Delivery~Bread)

#3-2
#ANOVA (혹은 T-Test)를 수행하여 Garlic bread를 주문/비주문에 따라 
#피자 배달 평균시간에 차이가 유효한지를 설명
br = aov(Delivery~Bread)
summary(br)
round(tapply(Delivery, Bread, mean),2)
detach(piz)
