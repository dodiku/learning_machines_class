#!/usr/bin/python

'''
Learning Machines
Taught by Patrick Hebron at NYU ITP

Example code for The Great Hyperparameter Hunt assignment.
'''

from Mnist import *
from Supervised import *
from Unsupervised import *
import numpy as np
np.set_printoptions( precision = 3, suppress = True )


'''
NOTE:

The hyperparameter configurations below are for demonstration purposes only.
Your job is to find better ones.

Please see README for more information on this assignment.
'''

class StackedRbm():

    __jobs_queue = []

    def add_job(self, mnist_use_threshold, rbm_is_continuous, rbm_visible_size, rbm_hidden_size, rbm_batch_size, rbm_learn_rate, rbm_cd_steps, rbm_training_epochs, rbm_report_freq, mlp_layer_sizes, mlp_batch_size, mlp_learn_rate, mlp_training_epochs):
        obj = {
            'mnist_use_threshold': mnist_use_threshold,     # Bool
            'rbm_is_continuous': rbm_is_continuous,         # Bool
            'rbm_visible_size': rbm_visible_size,           # int (e.g. 784)
            'rbm_hidden_size': rbm_hidden_size,             # int (e.g. 50)
            'rbm_batch_size': rbm_batch_size,               # int (e.g. 10)
            'rbm_learn_rate': rbm_learn_rate,               # float (e.g. 0.01)
            'rbm_cd_steps': rbm_cd_steps,                   # int (e.g. 1)
            'rbm_training_epochs': rbm_training_epochs,     # int (e.g. 100)
            'rbm_report_freq': rbm_report_freq,             # int (e.g. 1)
            'mlp_layer_sizes': mlp_layer_sizes,             # list (e.g. [20, 10])
            'mlp_batch_size': mlp_batch_size,               # int (e.g. 10)
            'mlp_learn_rate': mlp_learn_rate,               # float (e.g. 0.05)
            'mlp_training_epochs': mlp_training_epochs      # int (e.g. 100)
        }

        self.__jobs_queue.append(obj)
        return

    def jobs_left(self):
        print ('🔄  there are {} jobs left\n'.format(len(self.__jobs_queue)))
        return

    def run_all_jobs(self):
        for obj in self.__jobs_queue:
            self.single_run(obj)
            self.jobs_left()
            if len(self.__jobs_queue) > 0:
                self.__jobs_queue = self.__jobs_queue[:-1]
            else:
                print ('\n❤️  all jobs ran successfully\n')

        return

    def single_run(self, obj):

        # General settings (you CAN change these):
        mnist_use_threshold = obj['mnist_use_threshold']

        # RBM hyperparameters (you CAN change these):
        rbm_is_continuous	= obj['rbm_is_continuous']
        rbm_visible_size	= obj['rbm_visible_size']
        rbm_hidden_size		= obj['rbm_hidden_size']
        rbm_batch_size		= obj['rbm_batch_size']
        rbm_learn_rate		= obj['rbm_learn_rate']
        rbm_cd_steps		= obj['rbm_cd_steps']
        rbm_training_epochs = obj['rbm_training_epochs']
        rbm_report_freq		= obj['rbm_report_freq']
        rbm_report_buffer	= rbm_training_epochs

        # MLP hyperparameters (you CAN change these):
        mlp_layer_sizes		= [ rbm_hidden_size ]
        for layer_size in obj['mlp_layer_sizes']:
            mlp_layer_sizes.append(layer_size)

        mlp_batch_size		= obj['mlp_batch_size']
        mlp_learn_rate		= obj['mlp_learn_rate']
        mlp_training_epochs = obj['mlp_training_epochs']
        mlp_report_freq		= 1
        mlp_report_buffer	= mlp_training_epochs

        # MNIST training example counts (you CANNOT change these):
        mnist_num_training_examples	  = 10000
        mnist_num_validation_examples =	 5000
        mnist_num_testing_examples	  =	 5000

        # Load MNIST dataset:
        mnist = Mnist( mnist_use_threshold )

        training_digits,   training_labels	 = mnist.getTrainingData( mnist_num_training_examples )
        validation_digits, validation_labels = mnist.getValidationData( mnist_num_validation_examples )
        testing_digits,	   testing_labels	 = mnist.getTestingData( mnist_num_testing_examples )

        # Initialize and train RBM:
        rbm_name = 'rbm_' + str(rbm_visible_size) + '_' + str(rbm_hidden_size)
        rbm = Rbm( rbm_name, rbm_visible_size, rbm_hidden_size, rbm_is_continuous )
        rbm.train( training_digits, validation_digits, rbm_learn_rate, rbm_cd_steps, rbm_training_epochs, rbm_batch_size, rbm_report_freq, rbm_report_buffer )

        # Encode datasets with RBM:
        _, training_encodings = rbm.getHiddenSample( training_digits )
        _, validation_encodings = rbm.getHiddenSample( validation_digits )
        _, testing_encodings = rbm.getHiddenSample( testing_digits )

        # Initialize and train MLP:
        mlp_name = 'mlp_' + '_'.join( str(i) for i in mlp_layer_sizes )
        mlp = Mlp( mlp_name, mlp_layer_sizes, 'sigmoid' )
        mlp.train( training_encodings, training_labels, validation_encodings, validation_labels, mlp_learn_rate, mlp_training_epochs, mlp_batch_size, mlp_report_freq, mlp_report_buffer )

        # Perform final test:
        testing_guesses = mlp.predict( testing_encodings )
        testing_error = mlp.getErrorRate( testing_labels, testing_guesses )
        testing_accuracy = mnist_get_accuracy( testing_labels, testing_guesses )
        print ('Final Testing Error Rate: %f' % ( testing_error ))
        print ('Final Testing Accuracy: %f' % ( testing_accuracy ))
        print ('🏁  run has ended successfully')


        return


jobs = StackedRbm()
jobs.add_job(True, False, 784, 200, 20, 0.02, 1, 200, 1, [20, 20, 10], 20, 0.03, 200)
jobs.add_job(False, False, 784, 50, 10, 0.01, 1, 200, 1, [20, 10], 10, 0.02, 200)
jobs.add_job(True, True, 784, 200, 12, 0.02, 2, 150, 1, [12,12,10], 12, 0.01, 150)
jobs.add_job(False, True, 784, 50, 10, 0.02, 1, 300, 1, [20, 10], 10, 0.05, 300)
jobs.add_job(False, False, 784, 80, 8, 0.01, 1, 100, 1, [8,6,10], 8, 0.05, 100)
jobs.add_job(True, True, 784, 25, 100, 0.01, 2, 300, 1, [10,20, 10], 100, 0.05, 300)
jobs.add_job(False, True, 784, 50, 10, 0.03, 1, 300, 1, [10,20, 10,20,10], 10, 0.05, 300)
jobs.add_job(True, False, 784, 50, 10, 0.02,3, 100, 1, [20, 10], 10, 0.01, 100)
jobs.add_job(True, False, 784, 50, 4, 0.02,3, 100, 1, [4,4,4,4,4,10], 4, 0.01, 100)
jobs.add_job(False, True, 784, 50, 10, 0.01, 1, 100, 1, [20, 10], 10, 0.05, 100)
jobs.add_job(False, True, 784, 50, 10, 0.1, 1, 100, 1, [10, 10, 10], 10, 0.01, 100)
jobs.run_all_jobs()
