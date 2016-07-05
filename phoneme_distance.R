# read data
phoneme.data <- read.csv('output/distance_scores.csv', encoding='UTF-8')
rownames(phoneme.data) <- phoneme.data[,1] # name rows
phoneme.data[,1] <- NULL

# scale, making the largest value 0.99
phoneme.data$distance <- (phoneme.data$distance / max(phoneme.data$distance)) * 0.99

# linear model
distance.lm <- lm(distance ~ ., data=phoneme.data)
#distance.lm <- lm(I(distance - 1.0) ~ 0 + ., data=phoneme.data) # intercept at 1


# neural network
n <- names(phoneme.data)
f <- as.formula(paste('distance ~ ', paste(n[!n %in% "distance"], collapse=' + ')))
distance.nn <- neuralnet(f,data=phoneme.data, hidden=c(12,3), linear.output = T, lifesign="full")

# test lm & nn
predict.lm <- predict(distance.lm, phoneme.data)
MSE.lm <- sum((predict.lm - phoneme.data$distance)^2) / nrow(phoneme.data)

predict.nn_ <- compute(distance.nn, phoneme.data[,-ncol(phoneme.data)])
predict.nn <- predict.nn_$net.result *
  (max(phoneme.data$distance) - min(phoneme.data$distance)) + 
  min(phoneme.data$distance)
test.r <- phoneme.data$distance *
  (max(phoneme.data$distance) - min(phoneme.data$distance)) + 
  min(phoneme.data$distance)
MSE.nn <- sum((test.r - predict.nn)^2) / nrow(phoneme.data)

# compare
print(paste(MSE.lm, MSE.nn))

par(mfrow=c(1, 2))

plot(phoneme.data$distance, predict.nn, col='red', main='Real vs predicted NN', pch=18, cex=0.7)
abline(0, 1, lwd=2)
legend('bottomright', legend='NN', pch=18, col='red', bty='n')
#text(phoneme.data$distance, predict.nn, labels=rownames(phoneme.data), cex=0.8, pos=3)

plot(phoneme.data$distance, predict.lm, col='blue', main='Real vs predicted LM', pch=18, cex=0.7)
abline(0, 1, lwd=2)
legend('bottomright', legend='LM', pch=18, col='blue', bty='n', cex=.95)
#text(phoneme.data$distance, predict.lm, labels=rownames(phoneme.data), cex=0.8, pos=3)

par(mfrow=c(1,1))

plot(phoneme.data$distance, predict.nn, col='red', main='Real vs predicted NN & predicted LM', pch=18, cex=0.7)
points(phoneme.data$distance, predict.lm, col='blue', pch=18, cex=0.7)
abline(0, 1, lwd=2)
legend('bottomright', legend=c('NN','LM'), pch=18, col=c('red','blue'))
