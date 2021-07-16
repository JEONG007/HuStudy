setwd("C:/Users/Jeong/Documents/Hustar_Study/Rcode/Day4/")
getwd()

library(dplyr)

install.packages("corrplot")
library(corrplot)

#1
sat2010 = read.csv("SAT_2010.csv")

#1-A
#해당 데이터에서 중복 데이터가 존재하는가? 
dupes = duplicated(sat2010)
table(dupes)
which(dupes == "TRUE")

#1-B
#해당 데이터에서 문자 변수는 총 몇 개가 있는가? 
str(sat2010)

#1-C
#결측치가 있는가? 
sat_na_count = sapply(sat2010, function(y)sum(length(which(is.na(y)))))
sat_na_df = data.frame(sat_na_count)
View(sat_na_df)

#1-D
#변수 read와 변수 math와의 상관계수가 0.9보다 큰 변수를 모두 찾아라.
attach(sat2010)
cor(select(sat2010,-state),read)
cor(select(sat2010,-state),math)
detach(sat2010)

#2
happy = read.csv("happy2020.csv")

#2-A
#결측치가 있는가?
happy_na_count = sapply(happy, function(y)sum(length(which(is.na(y)))))
happy_na_df = data.frame(happy_na_count)
View(happy_na_df)

#2-B
#행복도(ladder score)에 가장 큰 영향을 미치는 요소 세가지를 상관 분석을 통해서 도출해내라
attach(happy)
newHappy = happy[, !sapply(happy, class) == 'character']
corrplot(cor(newHappy,Ladder.score),method = "number")

plot(Ladder.score, Logged.GDP.per.capita) + abline(lm(Logged.GDP.per.capita~Ladder.score))
cor(Ladder.score, Logged.GDP.per.capita)
plot(Ladder.score, Social.support)+ abline(lm(Social.support~Ladder.score))
cor(Ladder.score, Social.support)
plot(Ladder.score, Healthy.life.expectancy) + abline(lm(Healthy.life.expectancy~Ladder.score))
cor(Ladder.score, Healthy.life.expectancy)

#2-C
#행복지수가 가장 높은 나라와 낮은 나라는 어디이며 각각의 행복지수는 몇인가?
c2 = select(happy, Country.name, Ladder.score)
filter(c2, Ladder.score == max(Ladder.score))
filter(c2, Ladder.score == min(Ladder.score))

#2-E
#B에서 구한 세가지 요소를 이용하여 종속변수를 행복도로 두고 회귀모형을 수행하고 해석하라
summary(lm(Ladder.score~Logged.GDP.per.capita))
summary(lm(Ladder.score~Social.support))
summary(lm(Ladder.score~Healthy.life.expectancy))

my_cols <- c("#00AFBB", "#E7B800", "#FC4E07")  
d2 = c("Logged.GDP.per.capita", "Social.support", "Healthy.life.expectancy","Ladder.score")
pairs(happy[d2], col = my_cols, pch=19)

detach(happy)