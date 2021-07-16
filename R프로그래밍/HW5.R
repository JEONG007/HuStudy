setwd("C:/Users/Jeong/Documents/Hustar_Study/Rcode/Day5/")
getwd()

library(dplyr)
library(ggplot2)

#1
#Is monthly data or daily data? 
tsla = read.csv("TSLA.csv")
head(tsla)

#2
#what is the date with the highest price? 
attach(tsla)
data = select(tsla, Date, High, Low)
filter(data, High == max(High))
filter(data, Low == max(Low))

#3
#Any trend you find out from the given information in kaggle?  
tsla$Date = as.Date(tsla$Date)
ggplot(tsla, mapping=aes(x=Date,y=High))+ geom_line(aes(x=Date,y=High))

cor(Low, High)

detach(tsla)