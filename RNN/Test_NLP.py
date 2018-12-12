import itertools
from Preprocessing_NLP import test

Delai = [365,730,1000]
Regularizer = [0.0003,0.001,0.003]
Learning_rate = [0.003,0.01,0.03]
Width = [16,64,256]
Layers = [2]
j = 0
for i in itertools.product(Delai, Regularizer, Learning_rate,Width, Layers):
    test(training_samples = 10000,
         validation_samples = 2000,
         maxlen = 200,
         max_words = 10000,
         delai = i[0],
         epochs = 50,
         embedding_dim = 200,
         regularizer = i[1],
         learning_rate = i[2],
         batch_size = 200,
         width = i[3],
         layers = i[4])
    j = j + 1
    print("Calculation for the parameters {} is done.".format(i))
    print(round(100*j/(len(Delai)*len(Regularizer)*len(Learning_rate)*len(Width)*len(Layers)),4),"% of the tests have been done.")
