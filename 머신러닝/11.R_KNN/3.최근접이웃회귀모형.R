df<-read.csv("c:/data/ozone/ozone2.csv")
head(df)

#필드 제거
library(dplyr)
df <- df %>% select(-Month, -Day, -Result)

library(caret)
set.seed(123) # 랜덤 시드 고정

#학습용:검증용 8:2로 구분
idx_train <- createDataPartition(y=df$Ozone, p=0.8, list=F)

#학습용
train <- df[idx_train, ]
X_train <- train[, -1]
y_train <- train[, 1]

#검증용
test <- df[-idx_train, ]
X_test <- test[, -1]
y_test <- test[, 1]

head(X_train)
head(y_train)

#분류 정확도
#install.packages("FNN")
library(FNN)
# 분류 정확도를 저장할 비어있는 벡터
acc <- NULL

for (i in c(1:10)){
	set.seed(123) # 재현성을 위해 설정
	model <- knn.reg(X_train, X_test, y_train, k=i)
	
	# mse
	m <- mean((model$pred - y_test)^2) 
 	acc <- c(acc, m)
}

# 차트를 그리기 위해 데이터프레임으로 변환
df <- data.frame(k=c(1:10), mse=acc)
df
# k에 따른 분류 정확도 그래프 그리기
plot(mse ~ k, data=df, type="o", pch=20, main="최적의 k값", col="red")

# 그래프에 k 라벨링
with(df, text(mse ~ k, labels=c(1:10), pos=1, cex=0.7))

#최적의 k
n <- min(df[df$mse %in% min(acc), "k"])
df[n, ]

#최적의 k일 때의 KNN 모형
model <- knn.reg(X_train, X_test, y_train, k=10)
model$pred # 예측값

#Mean Squared Error(평균제곱오차)
mean((model$pred - y_test)^2)
sqrt(mean((model$pred - y_test)^2))
