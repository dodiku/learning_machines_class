from mlp import *
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

db_path = 'db/car.data'
df = pd.read_csv(db_path)

# splitting raw data from classes
inputs = df.iloc[:,:6]
outputs = df.iloc[:,6]

# converting data to nums
conversion = [['vhigh', 'high', 'med', 'low'],
['vhigh', 'high', 'med', 'low'],
['0', '1','2', '3', '4', '5more'],
['2', '4', 'more'],
['small', 'med', 'big'],
['low', 'med', 'high']]

conversion_outputs = ['unacc', 'acc', 'good', 'vgood']

for i in range(len(conversion)):
    inputs.iloc[:,i] = list(map(lambda x: conversion[i].index(x), inputs.iloc[:,i]))

outputs = list(map(lambda x: conversion_outputs.index(x), outputs))
outputs = pd.Series(outputs)

# splitting the data to training and validation
x_training, x_validation, y_training, y_validation = train_test_split(inputs, outputs, test_size=0.25, random_state=42, shuffle=True)

# converting all to numpy array
x_training = np.array(x_training).T
x_validation = np.array(x_validation).T
y_training = np.array(y_training).reshape(1,-1)
y_validation = np.array(y_validation).reshape(1,-1)

# Set hyperparameters:
sample_size = 6
output_size = 1
example_cnt = x_training.shape[1]
batch_size  = 4
epoch_cnt   = 10000
report_freq = 40
learn_rate  = 0.05
hidden_layers = [8,12,8]

# creating configurations list
settings = []
settings.append(sample_size)
for n in hidden_layers:
    settings.append(n)
settings.append(output_size)

# Construct MLP:
mlp = Mlp( settings, "tanh" )

# Construct dataset:
training_inputs  = x_training
training_outputs = y_training

# Train MLP:
mlp.train( training_inputs, training_outputs, learn_rate, epoch_cnt, batch_size, report_freq )

# Make predictions:
training_guesses = mlp.predict( x_validation )

# Print correct and predicted outputs:
predictions = np.round(training_guesses) == y_validation
count = 0
for p in predictions[0]:
    if p == True:
        count+=1

print ('🏁  {} percent error rate.\n   {} correct predictions out of {} validation samples.'.format(count/y_validation.shape[1]*100,count,y_validation.shape[1]))
# print (( "Outputs: %s\nGuesses: %s\n" ) % ( training_outputs, training_guesses ))
print ('\nSettings:')
print ('batch_size:', batch_size)
print ('epoch_cnt:', epoch_cnt)
print ('learn_rate:', learn_rate)
print ('hidden_layers:', hidden_layers)

print ('\n\n🌆  yay!\n\n')
