'''
At least 20 epochs are required before the generated text
starts sounding coherent.

It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.

If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function
import random
import sys
import io
import re
import numpy as np

from keras.callbacks import LambdaCallback
from keras.initializers import Constant
from keras.layers import *
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils.data_utils import get_file
from keras.utils.np_utils import to_categorical

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
#TRIAL
alloweddepts="HUMBIO,PWR,BIO,MS&E,POLISCI,ME,EDUC,HISTORY,CEE,CS".split(",")

#collect all reviews and the corresponding departments they belong to in departments
reviewsText = []
departments = []
import csv
with open('oneReviewPerColDF.csv', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in read:
#        course_code = row[1] - commented out because we are not classifying by course, but by department
        department = row[2]
        review = row[3]
        if department not in alloweddepts:
            continue
        reviewsText.append(review)
        departments.append(department)

#remove header
reviewsText = reviewsText[1:]
departments = departments[1:]

max_features = 20000 # this is the number of words we care about

tokenizer = Tokenizer(num_words=max_features, split=' ', filters=' ')
tokenizer.fit_on_texts(reviewsText)

print(reviewsText[0])

sequences = tokenizer.texts_to_sequences(reviewsText)

print(sequences[0])

seq_len=256

X = pad_sequences(sequences, maxlen=seq_len)

print(X[0])

print(len(X), len(reviewsText))

uniqDepart = sorted(list(set(departments)))
depart_indices = dict((d, i) for i, d in enumerate(uniqDepart))

y = np.zeros((len(X), len(uniqDepart)), dtype=np.bool)
for i, depart in enumerate(departments):
    y[i, depart_indices[depart]] = 1

# 90/10 train/test split
X_train, X_test, y_train, y_test, text_train, text_test = train_test_split(X, y, reviewsText, test_size=0.1)

print("what",departments[0])
print(uniqDepart.index(departments[0]))
print(y[0])
print(uniqDepart)
print(len(uniqDepart))

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

embeddings_index = {}
f = open('glove.6B.100d.txt')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))
num_words = min(max_features, len(word_index)) + 1
print(num_words)

embedding_dim = 100

# first create a matrix of zeros, this is our embedding matrix
embedding_matrix = np.zeros((num_words, embedding_dim))

# for each word in out tokenizer lets try to find that work in our w2v model
for word, i in word_index.items():
    if i > max_features:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # we found the word - add that words vector to the matrix
        embedding_matrix[i] = embedding_vector
    else:
        # doesn't exist, assign a random vector
        embedding_matrix[i] = np.random.randn(embedding_dim)

for x in sequences[0]:
    print(x)
    print(embedding_matrix[x])


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(Embedding(num_words,
                    embedding_dim,
                    embeddings_initializer=Constant(embedding_matrix),
                    input_length=seq_len,
                    trainable=True))
model.add(LSTM(128, input_shape=(seq_len, embedding_dim)))
model.add(Dense(len(uniqDepart), activation='softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

def game():
    right=0
    p=model.predict(X_test, verbose=0)
    m={}
    for ind in range(len(X_test)):
        realCat = y_test[ind].tolist().index(1)
        print("Real department:",uniqDepart[realCat])
        pred=p[ind].tolist()
        category=pred.index(max(pred))
        print("Predicted department:", uniqDepart[category])
        if uniqDepart[realCat] not in m:
            m[uniqDepart[realCat]] = {}
        if uniqDepart[category] not in m[uniqDepart[realCat]]:
            m[uniqDepart[realCat]][uniqDepart[category]]=0
        m[uniqDepart[realCat]][uniqDepart[category]]+=1
        if realCat == category:
            right+=1
    print(right)
    print(right*1.0/len(X_test))
    print(m)

def on_epoch_end(epoch, _):

    # Function invoked at end of each epoch. Prints generated text.
    print()
    print('----- Generating text after Epoch: %d' % epoch)
    game()

game()

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model.fit(X_train, y_train,
          batch_size=128,
          epochs=60,
          callbacks=[print_callback])
