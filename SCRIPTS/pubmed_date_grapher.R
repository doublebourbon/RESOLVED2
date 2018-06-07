setwd("RESOLVED²")
require(ggplot2)

miss = read.table(file = "PUBMED_DATA/pubmed_data_2606_noDRUG.txt", header = TRUE, as.is = TRUE, na.strings = "NA", sep = "\t")
pubmed = read.table(file = "PUBMED_DATA/pubmed_data_2606.txt", as.is = TRUE)




nodrug = as.data.frame((table(miss$Year_publication)))
colnames(nodrug) = c("Publication_Year", "Freq")


all = as.data.frame((table(pubmed$Year_publication)))
colnames(all) = c("Publication_Year", "Freq")



df1 <- data.frame(Match=c(rep("No_Match",times = length(nodrug$Publication_Year)),
                          rep("All",times = length(all$Publication_Year))),
                  Publication_Year=c(as.numeric(as.character(nodrug$Publication_Year)),
                                     as.numeric(as.character(all$Publication_Year))),
                  Freq=c(nodrug$Freq, all$Freq))

df2 <- data.frame(Match=c(rep("No_Match",times = length(nodrug$Publication_Year)), rep("All",times = length(all$Publication_Year))),
                  Publication_Year=c(as.numeric(as.character(nodrug$Publication_Year)), as.numeric(as.character(all$Publication_Year))),
                  Freq=c(nodrug$Freq/length(miss$PMID), all$Freq/length(pubmed$PMID)))

df3 <- data.frame(Match=c(rep("No_Match",times = length(nodrug$Publication_Year))),
                  Publication_Year=c(as.numeric(as.character(nodrug$Publication_Year))),
                  Freq=c(nodrug$Freq)/length(miss$PMID))

df4 <- as.data.frame((table(pubmed$Year_publication) - table(miss$Year_publication))/table(pubmed$Year_publication))


df5 <- as.data.frame((table(pubmed$Year_publication) - table(miss$Year_publication)))



ggplot(data=df1, aes(x=Publication_Year, y=Freq, fill=Match)) +
  geom_bar(stat="identity", position=position_dodge()) + 
  theme(axis.text.x = element_text(angle=65, vjust=0.6)) + 
  geom_smooth(method='auto')

ggplot(data=df2, aes(x=Publication_Year, y=Freq, fill=Match)) +
  geom_bar(stat="identity", position=position_dodge()) + 
  theme(axis.text.x = element_text(angle=65, vjust=0.6))+ 
  geom_smooth(method='auto') + 
  xlab(label = "Publication Year") + 
  ylab(label = "Percentage of sample")

ggplot(data=df3, aes(x=Publication_Year, y=Freq, fill=Match)) +
  geom_bar(stat="identity", position=position_dodge()) + 
  theme(axis.text.x = element_text(angle=65, vjust=0.6))+ 
  geom_smooth(method='auto')

ggplot(data=df3, aes(x=Publication_Year, y=Freq*100)) +
  geom_bar(stat="identity", position=position_dodge(),
           fill="deepskyblue3") + 
  theme(axis.text.x = element_text(angle=65, vjust=0.6),
        axis.title.y=element_text(angle=90, size=8))+ 
  geom_smooth(method='auto') +
  xlab(label = "Publication Year") + 
  ylab(label = "") +
  labs(title = "Percentage of non-matching abstacts relative to total non-matching abstracts")


ggplot(data=df4, aes(x=Var1, y=Freq*100)) +
  geom_bar(stat="identity", fill="tomato3") +
  theme(axis.text.x = element_text(angle=65, vjust=0.6))+ 
  geom_smooth(method='loess') + 
  xlab(label = "Publication Year") + 
  ylab(label = "Percentage of matching abstacts") +
  labs(title = "Percentage of matching abstract by year of publication")

ggplot(data=df5, aes(x=Var1, y=Freq)) +
  geom_bar(stat="identity", fill="tomato3") +
  theme(axis.text.x = element_text(angle=65, vjust=0.6))+ 
  geom_smooth(method='loess') + 
  xlab(label = "Publication Year") + 
  ylab(label = "Number of matching abstacts") +
  labs(title = "Number of matching abstract by year of publication")

#WITH UPDATED DATA



associations = read.table(file = "PUBMED_DATA/pubmedNdrugs_3.txt",
                       sep = "\t",
                       col.names = c("PMID","Year","Title", "DrugAlias"),
                       as.is = TRUE,
                       comment.char = "",
                       quote = "", encoding = "utf-8"
                       )




citations = read.table(file = "PUBMED_DATA/drug_counter_2.txt",
                       sep = "\t",
                       encoding = "utf-8",
                       col.names = c("Drug Alias", "Citations in abstracts"),
                       as.is = TRUE,
                       comment.char = "",
                       quote = "",
                       skipNul = TRUE)

summary(citations)

sum(citations$Citations.in.abstracts)

graph = function(title, range) {
  topDrugs = citations[range,]
  
  topPubmed = c()
  for (drugname in topDrugs$Drug.Alias) {
    topPubmed = c(topPubmed, associations$PMID[grep(pattern = drugname,
                                                    x = associations$DrugAlias,
                                                    fixed = TRUE,
                                                    ignore.case = FALSE)])
  }
  
  head(topPubmed)
  topPubmed = unique(sort(topPubmed))
  topArticles = pubmed[0,]
  
  
  topArticles = pubmed[pubmed$PMID %in% topPubmed,]
  
  
  topArticles$Drug = associations$DrugAlias[associations$PMID %in% topArticles$PMID]
  
  
  all = as.data.frame(table(topArticles$Year_publication))
  
  colnames(all) = c("Year", "Freq")
  
  for (date in seq(min(pubmed$Year_publication), max(pubmed$Year_publication))) {
    if (!(date %in% all$Year)) all = rbind(all, data.frame(Year = as.factor(date), Freq = 0))
  }
  
  all$Year = as.numeric(as.character(all$Year))
  all = all[order(all$Year),]
  
  all$FreqYear = all$Freq/as.data.frame(table(pubmed$Year_publication))[,2]
  table(pubmed$Year_publication)
  all$FreqYear
  
  ggplot(data = all, aes(x = Year, y = FreqYear*100)) +
    geom_point() +
    geom_smooth(method="loess", linetype="dashed",
                color="darkred", fill="blue") + 
    ylab(label = "Percentage of citation through abstract corpus by year") +
    xlab(label = "Publication Year") +
    labs(title =title)
}

graph(title = "Top 15 most frequent drugs", range = 1:15)
