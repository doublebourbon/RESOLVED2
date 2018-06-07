setwd("RESOLVED²")

require(ggplot2)

 
# Probleme avec le character "beta" dans le fichier, car apparement R a du mal avec
# les encodages sur windows
# Les resultats peuvent sont encore exploitables car l erreur ne se produit pas avant la 678 ligne
# et n influence pas notre graphe

citations = read.table(file = "PUBMED_DATA/drug_counter_2.txt",
                       sep = "\t",
                       encoding = "utf-8",
                       col.names = c("Drug Alias", "Citations in abstracts"),
                       as.is = TRUE,
                       comment.char = "",
                       quote = ""
                       )


summary(citations)

citations[1:50,]

top50 = citations[1:50,]
top200 = citations[1:200,]



ggplot(data = top50, aes(x = reorder(Drug.Alias,-Citations.in.abstracts), y = Citations.in.abstracts)) +
  geom_bar(stat="identity", width=0.6, fill="tomato3") +
  ylab(label = "Citations in abstracts") +
  xlab(label = "Drug alias") +
  theme(axis.text.x = element_text(angle=90, hjust=1, size=7)) +
  scale_y_continuous(breaks = c(0,100,10, 40, 70,80, 60, 50, 30, 20))


ggplot(data = top200, aes(x = reorder(Drug.Alias,-Citations.in.abstracts), y = Citations.in.abstracts)) +
  geom_bar(stat="identity", width=0.6, fill="tomato3") +
  ylab(label = "Citations in abstracts") +
  xlab(label = "Drug alias") +
  theme(axis.text.x = element_blank()) +
  scale_y_continuous(breaks = c(0,100,10, 40, 70,80, 60, 50, 30, 20, 3))
