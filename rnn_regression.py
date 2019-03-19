#adapted from Kaggle (simple LSTM for text classification) and machinelearningmastery.com (glove)
#https://www.kaggle.com/kredy10/simple-lstm-for-text-classification
#https://machinelearningmastery.com/use-word-embedding-layers-deep-learning-keras/

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.layers import Bidirectional
from keras.utils import to_categorical

#reads in data from small_fic_dataset.tsv
#df = pd.read_csv("small_fic_dataset.tsv",delimiter='\t',encoding='latin-1')
df = pd.read_csv("records:1-180.tsv",delimiter='\t',encoding='latin-1')
df.head()

#visualize data
df.info()
sns.countplot(df.MAINTAG)
plt.xlabel('Label')
plt.title('Number of fics in each rating')
plt.show()
#get input and label vectors
X = df.TEXT
Y = []
for index in range(len(df.MAINTAG)):
        if df.MAINTAG[index]=="General Audiences":
                Y.append(0)
        elif df.MAINTAG[index]=="Teen And Up Audiences":
                Y.append(1)
        elif df.MAINTAG[index]=="Mature":
                Y.append(2)
        else:
                Y.append(3)

#split into training and test sets
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,shuffle=True)


#parameters for embedding and tokenizing 
max_len = 220
tok = Tokenizer(lower=True)
tok.fit_on_texts(X_train)
max_words = len(tok.word_index.items())+1
print(max_words)

#get glove embeddings
embeddings_index = dict()
f = open('glove.6B.100d.txt')
for line in f:
	values = line.split()
	word = values[0]
	coefs = np.asarray(values[1:], dtype='float32')
	embeddings_index[word] = coefs
f.close()
embedding_matrix = np.zeros((max_words,100))
for word,i in tok.word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

#makes padded sequences so all inputs are of the same length
sequences = tok.texts_to_sequences(X_train)
sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)

test_sequences = tok.texts_to_sequences(X_test)
test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)
print("printing first test sequence matrix")
print(test_sequences_matrix[0])
print("done printing first test sequence matrix")

def RNN():
    inputs = Input(name='inputs',shape=[max_len])
    layer = Embedding(max_words,100,weights=[embedding_matrix],input_length=max_len)(inputs)
    layer = Bidirectional(LSTM(64))(layer)
    layer = Dense(256,name='FC1')(layer)
    layer = Activation('relu')(layer)
    layer = Dropout(0.5)(layer)
    layer = Dense(1,name='out_layer')(layer)
    layer = Activation('linear')(layer)
    model = Model(inputs=inputs,outputs=layer)
    return model

model = RNN()
model.summary()
model.compile(loss='mean_squared_error',optimizer=RMSprop(lr=0.001),metrics=['accuracy'])
#trains model
model.fit(sequences_matrix,Y_train,epochs=6,validation_split=0.3,shuffle=True)
Y_hat = model.predict(test_sequences_matrix)
X_list = list(X_test)
for i in range(50):
        print("~")
        print(i)
        print(X_list[i])
        print(Y_test[i])
        print(Y_hat[i])
#tests model and prints metrics
accr = model.evaluate(test_sequences_matrix,Y_test)
print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))
