#adapted from Kaggle (simple LSTM for text classification)
#https://www.kaggle.com/kredy10/simple-lstm-for-text-classification

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
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
#%matplotlib inline
df = pd.read_csv("small_fic_dataset.tsv",delimiter='\t',encoding='latin-1')
df.head()
#df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'],axis=1,inplace=True)
df.info()
sns.countplot(df.MAINTAG)
plt.xlabel('Label')
plt.title('Number of fics in each rating')
plt.show()
X = df.TEXT
Y = df.MAINTAG
le = LabelEncoder()
Y = le.fit_transform(Y)
Y = Y.reshape(-1,1)
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,shuffle=True)
print(Y_train)
Y_train = to_categorical(Y_train, num_classes=4, dtype='float32')
print(Y_train)
Y_test = to_categorical(Y_test, num_classes=4, dtype='float32')
#X_train=X
#Y_train=Y
max_words = 5000
max_len = 220
tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(X_train)
sequences = tok.texts_to_sequences(X_train)
sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)
def RNN():
    inputs = Input(name='inputs',shape=[max_len])
    layer = Embedding(max_words,500,input_length=max_len)(inputs)
    layer = LSTM(64)(layer)
    layer = Dense(256,name='FC1')(layer)
    layer = Activation('relu')(layer)
    layer = Dropout(0.5)(layer)
    layer = Dense(4,name='out_layer')(layer)
    layer = Activation('softmax')(layer)
    model = Model(inputs=inputs,outputs=layer)
    return model
model = RNN()
model.summary()
model.compile(loss='categorical_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])
model.fit(sequences_matrix,Y_train,epochs=10,validation_split=0.3,shuffle=True)
test_sequences = tok.texts_to_sequences(X_test)
#test_sequences = tok.texts_to_sequences(X_train)
test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)
accr = model.evaluate(test_sequences_matrix,Y_test)
#accr = model.evaluate(test_sequences_matrix,Y_train)
print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))
