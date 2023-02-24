
from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential
from keras.optimizers import Adam

# Create a sequential model
model = Sequential()

# Define the architecture of the model
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(16384, 129, 64, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='linear'))

# Compile the model
model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.001))

# Create training and testing data
x_train, x_test, y_train, y_test = train_test_split(data, hdv_fit, test_size=3 / 5)

# Fit the model to the training data
model.fit(x_train, y_train, epochs=10)  # , batch_size=32, validation_data=(x_test, y_test))

# Evaluate prediction accuracy of the model
prediction = model.predict(x_test)

# Plot the results
plt.scatter(prediction, y_test)
plt.xticks([])
plt.yticks([])
plt.show()
