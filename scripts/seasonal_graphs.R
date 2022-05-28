library(ggplot2)
library(tidyr)
library(reshape)

full_elo <- read_csv("~/activity/FantasyNBATools/YahooScraperElo/resources/full_elo.csv")

current_elos <- read_csv("~/activity/FantasyNBATools/YahooScraperElo/resources/weekly_elos.csv")

champions = list(
  "2014" = "Alison",
  "2015" = "Chris",
  "2016" = "Guillem",
  "2017" = "Ravi",
  "2018" = "John",
  "2019" = "Ravi",
  "2020" = "Sahil",
  "2021" = FALSE
)


process_df <- function(df, y, c){
  file_name = paste("./graphs/", as.character(y), sep = '')
  d = dim(df)
  week = d[2] -2
  names(df)[names(df) == "X"] <- "Players"
  
  
  df$Players = as.factor(df$Players)
  
  week_levs = c()
  week_nums = c()
  curr_week_fac = c()
  curr_week_levs = c()
  for (i in (1:(week + 1))){
    week_nums = c(week_nums, rep(i, d[1]))
    week_levs = c(week_levs, paste('week_', i - 1, sep=''))
  }
  
  week_factor = factor(week_nums)
  levels(week_factor) = week_levs
  
  Long_Elos = df %>% gather(week, elo, -c(Players))
  Long_Elos$week = week_factor
  Long_Elos$num_week = week_nums
  Long_Elos$Year = y
  Long_Elos$Champion = FALSE
  Long_Elos$Champion[Long_Elos$Players == champions[[as.character(y)]]] = TRUE
  Long_Elos$Champion_Shape = factor(as.integer(Long_Elos$Champion) + 1)
  levels(Long_Elos$Champion_Shape) = c("Loser", "Champion")
  if(y %in% c(2014, 2016)){
    Long_Elos$Scoring = 'Points'
  } else{
    Long_Elos$Scoring = '9Cat'
  }
  if(c){
    Long_Elos$Seasonal = 'Full'
    Long_Elos$num_week = -1 * Long_Elos$num_week
    file_name = paste(file_name, '_c', sep = '')
  } else{
    Long_Elos$Seasonal = 'Single'
    Long_Elos$num_week =  Long_Elos$num_week - 1
  }
  file_name = paste(file_name, '.pdf', sep = '')
  dev.new()
  #print( ggplot(Long_Elos, aes(x=week, y=elo, group=Players, color=Players, shape=Champion_Shape)) + geom_line() + geom_point())
  #ggsave(file_name, device='pdf', width=16, height=9, dpi=4000)
  return(Long_Elos)
}



singles = list()

cumulative = list()


setwd("/home/syrax/activity/FantasyNBATools/YahooScraperElo")

for (i in 2014:2021){
  single_file = paste('./resources/weekly_elos_', i, '.csv', sep='')
  single_df = read.csv(single_file)
  final_single_df = process_df(single_df, i, FALSE)
  singles[[as.character(i)]] = final_single_df
  cumulative_file = paste('./resources/weekly_elos_', i, '_c.csv', sep='')
  cumulative_df = read.csv(cumulative_file)
  final_cumulative_df = process_df(cumulative_df, i, TRUE)
  cumulative[[as.character(i)]] = final_cumulative_df
  graph_file = paste("./graphs/", as.character(i), "_double.pdf", sep="")
  double_df = rbind(final_single_df, final_cumulative_df)
  View(double_df)
  dev.new()
  print( ggplot(double_df, aes(x=num_week, y=elo, group=Players, color=Players, shape=Champion_Shape)) + geom_line() + geom_point())
  ggsave(graph_file, device='pdf', width=16, height=9, dpi=4000)
}

full_single_df = merge_all(singles)

full_cumulative_df = merge_all(cumulative)
full_cumulative_df$Year = as.factor(full_cumulative_df$Year)





d = dim(single_df)
week = d[2] - 2

names(single_df)[names(single_df) == "X"] <- "Players"


single_df$Players = as.factor(single_df$Players)

week_levs = c()
week_nums = c()
curr_week_fac = c()
curr_week_levs = c()
for (i in (1:(week + 1))){
  week_nums = c(week_nums, rep(i, d[1]))
  week_levs = c(week_levs, paste('week_', i - 1, sep=''))
}

week_factor = factor(week_nums)
levels(week_factor) = week_levs

Long_Elos = single_df %>% gather(week, elo, -c(Players))
Long_Elos$week = week_factor
Long_Elos$num_week = week_nums

ggplot(double_df, aes(x=num_week, y=Players, color=Players, size=elo)) + geom_point()
