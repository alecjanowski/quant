#!/usr/bin/env python
# coding: utf-8

# # This program predicts the last 20 (you can customize this) rows in a dependent data it loads. 

# ## What needs to be done next
# 1. Improve the prediction accuracy
# <br> We need to find the optimal combinatino of n_input (see the code), the number of neurons in the LSTM layer, the number of epochs.
# <br>
# <br> 
# 2. Incorporate metrics (hit rate, IC)
# <br>
# <br>
# 3. Test if this program works with the whole data. Right now, I have only tested with smaller data.

# This program is based on the following Udemy course's Section 9 Video 80-85: <br> https://www.udemy.com/share/101WWMB0Ydc1ZQRn4=/
# <br> You are guaranteed the 30-day money-back, so you can buy and return it within 30 days.

# Other articles I referenced to make this program:
# <br> https://machinelearningmastery.com/how-to-use-the-timeseriesgenerator-for-time-series-forecasting-in-keras/
# <br> https://qiita.com/ta1nakamura/items/11b53669ce48219d6475
# <br> https://www.dlology.com/blog/how-to-use-keras-timeseriesgenerator-for-time-series-data/

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dask.dataframe as dd
from tqdm import tqdm 
import warnings
warnings.filterwarnings(action = 'once')


# In[16]:


import pandas as pd
import numpy as np
from tqdm import tqdm

newTempDf2 = pd.read_csv("./TestData/Symbol_0.csv")
newTempDf2.drop(["Time"], axis=1, inplace = True)


# In[17]:


print(newTempDf2)


# In[25]:


# Convert dask arrays into numpy arrays
X = np.array(newTempDf2.iloc[:,1:])
y = np.array(newTempDf2.iloc[:,0:1])


# In[26]:


from sklearn.preprocessing import MinMaxScaler


# In[27]:


# Scale X and y, so that their ranges are within (0 ,1)
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

scaler_X.fit(X)
scaler_y.fit(y)

scaled_X = scaler_X.transform(X)
scaled_y = scaler_y.transform(y)


# In[29]:


# Split X and y into train and test
scaled_X_train = scaled_X[0:30000, :]
scaled_y_train = scaled_y[0:30000, :]
# I just chose 14 because the first 13 rows are filled with 0 (NAs)

scaled_X_test = scaled_X[30000:, :]
scaled_y_test = scaled_y[30000:, :]


# In[31]:


from keras.preprocessing.sequence import TimeseriesGenerator


# In[32]:


# Generate a TimeseriesGenerator, which learns the dependency between data
# In this case, the TimeseriesGenerator learns the dependency between scaled_X_train and scaled_y_train
n_input = 7 # 7 rows in scaled_X_train predicts 1 row in scaled_y_train
n_features = X.shape[1] # number of features—i.e. the number of colums of X

generator = TimeseriesGenerator(scaled_X_train, scaled_y_train, length=n_input, batch_size=1)
# "length": the number of the rows in scaled_X_train that are used for prediction
# "batch_size": the number of the labels (1 row in scaled_y_train)


# In[33]:


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


# In[34]:


# Create a neural network model
model = Sequential()

# Add a LSTM layer to the neural network. 150 is the number of neurons in the layer. You need to play around with the number to find the best one. But 100 is a good number to try first.
model.add(LSTM(150, activation = 'relu', input_shape=(n_input, n_features)))
# Add a normal neural network layer, which contains y.shape[1] neurons
model.add(Dense(y.shape[1]))
# Loss function (cost function) is mse(Mean squared error)
model.compile(loss='mse', optimizer='adam')


# In[35]:


# Show the shape of the neural network model we just created
model.summary()


# In[36]:


# Fit the model to the TimeseriesGenerator 30 times
#sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
model.fit_generator(generator,epochs=30)


# In[17]:


# Display how the loss decreases after each epoch
loss = model.history.history['loss']
epochs = range(len(loss))

plt.plot(epochs,loss)
plt.show()


# In[18]:


# This variable holds predicitons
test_predictions = [] 

# Use last n_input points from the training set as a current_batch
first_eval_batch = scaled_X_train[-n_input:, :]
current_batch = first_eval_batch.reshape(1, n_input, n_features)
# Reshape so that the shape of first_eval_batch matches that of X of TimeseriesGenerator

# Predict len(scaled_y_test) datapoints
for i in range(len(scaled_y_test)):
    current_pred = model.predict(current_batch)[0]
    
    # Store the current prediction
    test_predictions.append(current_pred)
    
    # Update the current batch 
    current_batch = np.append(current_batch[:,1:,:], [[scaled_X_test[i, :]]], axis=1)
    #  axis = 1 means that [[current_pred] will be added to the second dimension of current_batch[:,1:,:]


# In[19]:


# Scale back the predicted values so that they are in the orignal range 
true_predictions = scaler_y.inverse_transform(test_predictions)


# In[20]:


# Predicted rows
df_pred = pd.DataFrame(true_predictions)
df_pred


# In[37]:


# Original rows in the dependent data
df_dependent = pd.DataFrame(y[30000:, :])
df_dependent


# In[ ]:




