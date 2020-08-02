# -*- coding: utf-8 -*-
"""1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13Eb09hrVS8vIGBzZDIuY4AwuT2UHA-yJ
"""

import keras
from sklearn.model_selection import KFold
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD

# Load train and test dataset
def load_dataset():

	# load dataset
	(trainX, trainY), (testX, testY) = mnist.load_data()
 
	# reshape dataset to have a single channel
	trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
	testX = testX.reshape((testX.shape[0], 28, 28, 1))
 
	# one hot encode target values as the output has only 10 categories
	trainY = keras.utils.to_categorical(trainY)
	testY = keras.utils.to_categorical(testY)
 
	return trainX, trainY, testX, testY

# Scale pixels
def prep_pixels(train, test):

	# convert from integers to floats
	train_norm = train.astype('float32')
	test_norm = test.astype('float32')
 
	# normalize to range 0-1
	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0

	# return normalized images
	return train_norm, test_norm

# Define cnn model
def define_model():

	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
	model.add(MaxPooling2D((2, 2)))
	model.add(Flatten())
	model.add(Dense(10, activation='softmax'))
 
	# compile model
	opt = SGD(lr=0.01, momentum=0.9, nesterov=True)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
 
	return model

# Evaluate a model using k-fold cross-validation
def evaluate_model(dataX, dataY, n_folds=5):

	# prepare cross validation with random shuffle
	kfold = KFold(n_folds, shuffle=True, random_state=1)
 
	# enumerate splits
	for train_ix, test_ix in kfold.split(dataX):
   
		# define model
		model = define_model()
  
		# select rows for train and test of each fold
		trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]

		# fit model using the above selected data
		model.fit(trainX, trainY, epochs=10, batch_size=32, validation_data=(testX, testY), verbose=0)
  
		# evaluate model
		_, acc = model.evaluate(testX, testY, verbose=0)
  
		print('%.3f' % (acc * 100.0))
  
	return

# run the test harness for evaluating a model
def run_test_harness():

	# load dataset
	trainX, trainY, testX, testY = load_dataset()
 
	# prepare pixel data after feature engineering steps
	trainX, testX = prep_pixels(trainX, testX)
 
	# evaluate model
	evaluate_model(trainX, trainY)

# entry point, run the test harness
run_test_harness()

