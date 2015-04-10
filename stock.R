library(xts)

data2xts <- function(data) {
	data$Date <- as.Date(data$Date, format="%Y-%m-%d")
	data$Adj.Open <- round(data$Open * data$Adj.Close / data$Close, 2)
	data$Adj.High <- round(data$High * data$Adj.Close / data$Close, 2)
	data$Adj.Low <- round(data$Low * data$Adj.Close / data$Close, 2)
	columns <- c("Open", "Close", "High", "Low", "Volume", "Adj.Open", "Adj.Close", "Adj.High", "Adj.Low")
	head(xts(data[columns], order.by=data$Date))
}