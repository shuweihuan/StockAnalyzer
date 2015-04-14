library(xts)

data2xts <- function(data) {
	data$Date <- as.Date(data$Date, format="%Y-%m-%d")
	data$Adj.Open <- round(data$Open * data$Adj.Close / data$Close, 2)
	data$Adj.High <- round(data$High * data$Adj.Close / data$Close, 2)
	data$Adj.Low <- round(data$Low * data$Adj.Close / data$Close, 2)
	columns <- c("Open", "Close", "High", "Low", "Volume", "Adj.Open", "Adj.Close", "Adj.High", "Adj.Low")
	x <- xts(data[columns], order.by=data$Date)
	x$Index <- matrix(1:nrow(x))
	x$Adj.Close.Yesterday <- lag(x$Adj.Close)
	# x$Adj.Close.Diff.Daily <- diff(x$Adj.Close, lag=1)
	x$Adj.Close.Diff.Daily <- x$Adj.Close - x$Adj.Close.Yesterday
	x$Adj.Close.Diff.Daily.Rate <- x$Adj.Close.Diff.Daily / lag(x$Adj.Close)
	x$Adj.Open.Close.Diff <- x$Adj.Close - x$Adj.Open
	x$Adj.Open.Close.Diff.Rate <- x$Adj.Open.Close.Diff / x$Adj.Open
	x[1:20]
}

# source("stock.R")
# bidu <- read.csv("bidu.20150410.csv")
# b <- data2xts(bidu)