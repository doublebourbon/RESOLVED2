setwd("RESOLVED²")
require(ggplot2)

miss = read.table(file = "PUBMED_DATA/pubmed_data_2606_noDRUG.txt", header = TRUE, as.is = TRUE, na.strings = "NA", sep = "\t")
pubmed = read.table(file = "PUBMED_DATA/pubmed_data_2606.txt", as.is = TRUE)




nodrug = as.data.frame((table(miss$Year_publication)))
colnames(nodrug) = c("Publication_Year", "Freq")


all = as.data.frame((table(pubmed$Year_publication)))
colnames(all) = c("Publication_Year", "Freq")



df1 <- data.frame(Match=c(rep("No_Match",times = length(nodrug$Publication_Year)), rep("All",times = length(all$Publication_Year))),
                  Publication_Year=c(as.numeric(as.character(nodrug$Publication_Year)), as.numeric(as.character(all$Publication_Year))),
                  Freq=c(nodrug$Freq, all$Freq))

df2 <- data.frame(Match=c(rep("No_Match",times = length(nodrug$Publication_Year)), rep("All",times = length(all$Publication_Year))),
                  Publication_Year=c(as.numeric(as.character(nodrug$Publication_Year)), as.numeric(as.character(all$Publication_Year))),
                  Freq=c(nodrug$Freq/length(miss$PMID), all$Freq/length(pubmed$PMID)))

df3 <- data.frame(Match=c(rep("No_Match",times = length(nodrug$Publication_Year))),
                  Publication_Year=c(as.numeric(as.character(nodrug$Publication_Year))),
                  Freq=c(nodrug$Freq))



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


#WITH UPDATED DATA



associations = read.table(file = "PUBMED_DATA/pubmedNdrugs_2.txt",
                       sep = "\t",
                       col.names = c("PMID","Year","Title", "DrugAlias"),
                       as.is = TRUE,
                       comment.char = "",
                       quote = "", encoding = "utf-8"
                       )




citations = read.table(file = "PUBMED_DATA/drug_citation_counter.txt",
                       sep = "\t",
                       encoding = "utf-8",
                       col.names = c("Drug Alias", "Citations in abstracts"),
                       as.is = TRUE,
                       comment.char = "",
                       quote = "",
                       skipNul = TRUE)

summary(citations)

sum(citations$Citations.in.abstracts)

topDrugs = citations[1:10,]
sum(topDrugs$Citations.in.abstracts)

topDrugs$Drug.Alias
topPubmed = c()
for (drugname in topDrugs$Drug.Alias) {
  topPubmed = c(topPubmed, associations$PMID[grep(pattern = drugname,
                                                  x = associations$DrugAlias,
                                                  fixed = TRUE,
                                                  ignore.case = FALSE)])
}

head(topPubmed)

length(unique(sort(topPubmed)))
topPubmed = unique(sort(topPubmed))
topArticles = pubmed[0,]


topArticles = pubmed[pubmed$PMID %in% topPubmed,]

topArticles[1,]

topArticles$Drug = associations$DrugAlias[associations$PMID %in% topArticles$PMID]

topArticles[3,]



all = as.data.frame(table(topArticles$Year_publication))

colnames(all) = c("Year", "Freq")


ggplot(data = all, aes(x = Year, y = Freq)) +
  geom_point() +
  geom_smooth(method=lm, linetype="dashed",
              color="darkred", fill="blue")+
  stat_smooth()

