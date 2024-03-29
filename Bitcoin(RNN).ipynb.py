#Importing the Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Importing the Training Set
dataset_train = pd.read_csv('Bitcoin.csv')
training_set = dataset_train.iloc[:, 1:2]
training_set =training_set.to_numpy()


#feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0,1))
training_set_scaled = sc.fit_transform(training_set)

#Creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []
for i in range(60,1493):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train,y_train = np.array(X_train), np.array(y_train)

#Reshape 
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

#Part 2 - Building the RNN
#Importing the Keras libraries and packages
from keras.models import Sequential#层的顺序
from keras.layers import Dense#添加输出层
from keras.layers import LSTM
from keras.layers import Dropout#避免过度拟合

# Initialising the RNN
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units = 1))

#Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

#Fitting the RNN to the Training Set
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

#Getting the real Bitocin price of 2019
dataset_test = pd.read_csv('Bitcoin_Price_Test.csv')
real_Bitcoin_price = dataset_test.iloc[:,1:2].values


# Getting the predicted stock price of 2019
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 70):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_Bitcoin_price = regressor.predict(X_test)
predicted_Bitcoin_price = sc.inverse_transform(predicted_Bitcoin_price)

#Visualising the results
plt.plot(real_Bitcoin_price, color = 'red', label = 'Real Bitcoin Price')
plt.plot(predicted_Bitcoin_price, color = 'blue', label = 'Predicted Bitcoin Price')
plt.title('Bitcoin Price Prediction')
plt.xlabel('Time')
plt.ylabel('Bitcoin Price')
plt.legend()
plt.show()

import math
from sklearn.metrics import mean_squared_error
rmse = math.sqrt(mean_squared_error(real_Bitcoin_price,predicted_Bitcoin_price))






