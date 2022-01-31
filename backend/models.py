import numpy as np
import matplotlib.pyplot as plt
import keras
import keras.backend as K
from keras.applications.vgg16 import VGG16
from keras.layers import Input, Conv2D, Flatten, UpSampling2D
from keras.models import Model

class VGG_AE:

	def __init__(self,input_shape, weights="imagenet", encoder_trainable=False):
		self.encoder_trainable = encoder_trainable
		self.input_shape = input_shape
		self.base_model = None
		self.vgg_ae = None
		self.model = None
		self.weights = weights
		self.channels = self.input_shape[2]

	def create_model(self):
		"""Create the VGG-based autoencoder and assign starting weights to the model"""
		if self.weights == "imagenet":
			self.base_model = VGG16(weights="imagenet", input_shape=self.input_shape)
		else:
			self.base_model = VGG16(weights=None, input_shape=self.input_shape)
			self.base_model.load_weights(self.weights)

		for layer in self.base_model.layers:
			layer.trainable = self.encoder_trainable

		input_img = Input(shape = self.input_shape)
		self.vgg_ae = self.base_model.get_layer('block1_conv1')(input_img)
		self.vgg_ae = self.base_model.get_layer('block1_conv2')(self.vgg_ae)
		self.vgg_ae = self.base_model.get_layer('block1_pool')(self.vgg_ae)

		#    block2
		self.vgg_ae = self.base_model.get_layer('block2_conv1')(self.vgg_ae)
		self.vgg_ae = self.base_model.get_layer('block2_conv2')(self.vgg_ae)
		self.vgg_ae = self.base_model.get_layer('block2_pool')(self.vgg_ae)

		#    block3
		self.vgg_ae = self.base_model.get_layer('block3_conv1')(self.vgg_ae)
		self.vgg_ae = self.base_model.get_layer('block3_conv2')(self.vgg_ae)
		self.vgg_ae = self.base_model.get_layer('block3_conv3')(self.vgg_ae)    
		self.vgg_ae = self.base_model.get_layer('block3_pool')(self.vgg_ae)

		#    block4
		self.vgg_ae = self.base_model.get_layer('block4_conv1')(self.vgg_ae)
		self.vgg_ae = self.base_model.get_layer('block4_conv2')(self.vgg_ae)
		self.vgg_ae = self.base_model.get_layer('block4_conv3')(self.vgg_ae)    
		self.vgg_ae = self.base_model.get_layer('block4_pool')(self.vgg_ae)

		#    b l ock5
		self.vgg_ae = self.base_model.get_layer('block5_conv1')(self.vgg_ae)
		self.vgg_ae = self.base_model.get_layer('block5_conv2')(self.vgg_ae)
		self.vgg_ae = self.base_model.get_layer('block5_conv3')(self.vgg_ae)

		self.vgg_ae = self.base_model.get_layer('block5_pool')(self.vgg_ae)     
		self.vgg_ae = Conv2D(512, (3, 3), activation='relu', padding='same',name='latent')(self.vgg_ae)
		self.vgg_ae = UpSampling2D((2,2))(self.vgg_ae)

		  # Block 5
		self.vgg_ae = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock5_conv1')(self.vgg_ae)
		self.vgg_ae = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock5_conv2')(self.vgg_ae)
		self.vgg_ae = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock5_conv3')(self.vgg_ae)
		self.vgg_ae = UpSampling2D((2,2))(self.vgg_ae)

		# Block 4
		self.vgg_ae = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock4_conv1')(self.vgg_ae)
		self.vgg_ae = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock4_conv2')(self.vgg_ae)
		self.vgg_ae = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock4_conv3')(self.vgg_ae)
		self.vgg_ae = UpSampling2D((2,2))(self.vgg_ae)

		# Block 3
		self.vgg_ae = Conv2D(256, (3, 3), activation='relu', padding='same', name='dblock3_conv1')(self.vgg_ae)
		self.vgg_ae = Conv2D(256, (3, 3), activation='relu', padding='same', name='dblock3_conv2')(self.vgg_ae)
		self.vgg_ae = Conv2D(256, (3, 3), activation='relu', padding='same', name='dblock3_conv3')(self.vgg_ae)
		self.vgg_ae = UpSampling2D((2,2))(self.vgg_ae)     
		 
		# Block 2
		self.vgg_ae = Conv2D(128, (3, 3), activation='relu', padding='same', name='dblock2_conv1')(self.vgg_ae)
		self.vgg_ae = Conv2D(128, (3, 3), activation='relu', padding='same', name='dblock2_conv3')(self.vgg_ae)
		self.vgg_ae = UpSampling2D((2,2))(self.vgg_ae)        

		# Block 1
		self.vgg_ae = Conv2D(64, (3, 3), activation='relu', padding='same', name='dblock1_conv1')(self.vgg_ae)
		self.vgg_ae = Conv2D(self.channels, (3, 3), activation='relu', padding='same', name='dblock1_conv3')(self.vgg_ae)

		self.model = Model(input_img, self.vgg_ae)

		return self.model


		#def compile_model(self):
		#	self.model.compile(loss=self.loss, optimizer=self.optimizer)
