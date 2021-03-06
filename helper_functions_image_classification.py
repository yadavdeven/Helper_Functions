# -*- coding: utf-8 -*-
"""helper_functions_image_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1reCRErRetWdSKrtRvo_Qh9mx4jTax7Fx

## Functions for general image related projects:
"""

# Commented out IPython magic to ensure Python compatibility.
## importing libraries for getting suggestions:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import matplotlib.image as mpimg

## importing general python libraries:

import os
import random
import shutil
import glob
import itertools
import zipfile

## tensorflow imports:

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation,Dense,Flatten,BatchNormalization,Conv2D,MaxPool2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator

## function for extracting zip file:

def extract_zipped_file(file):
  zip_file = zipfile.ZipFile(file,"r")
  zip_file.extractall()
  zip_file.close()

## function for checking all folders and it's content:

def get_image_dataset_info(image_folder_name):
  for dirpath,folders,filenames in os.walk(image_folder_name):
    print(f"There are {len(folders)} directories and {len(filenames)} images in '{dirpath}'.")

## plotting loss curves:

def plot_loss_curves(history):

  loss = history.history["loss"]
  val_loss = history.history["val_loss"]

  accuracy = history.history["accuracy"]
  val_accuracy = history.history["val_accuracy"]

  epochs = range(len(history.history["loss"]))

  ##plotting for loss:

  plt.plot(epochs,loss)
  plt.plot(epochs,val_loss)
  plt.title("loss_curve")
  plt.xlabel("epochs")
  plt.ylabel("loss")
  plt.legend()

  ## plotting for accuracy:

  plt.figure()
  plt.plot(epochs,accuracy)
  plt.plot(epochs,val_accuracy)
  plt.title("accuracy_curve")
  plt.xlabel("epochs")
  plt.ylabel("accuracy")
  plt.legend()

## function for importing and resizing an image so as to be read by our model:

def load_resize_image(filename,img_size=224,rescale = True):

  ## parameters:
              # filename: takes image name in string format
              # img_size: final size of the image default is 224
              # rescale: whether or not to scale an image between (0,1) default is True
  
  img = tf.io.read_file(filename)            ## read an image
  img = tf.image.decode_image(img)           ## convert it into tensors
  img = tf.image.resize(img,[img_size,img,size])   ## resize the image
  if scale:
    img = img/255.
  else:
    return img

## Function for visualizing random images from our training dataset:

def visualize_training_images(train_dir,class_names):
  
  target_class = random.choice(class_names)
  target_dir = train_dir + target_class
  random_image = random.choice(os.listdir(target_dir))

  random_image_path = target_dir + "/" + random_image
  img = mpimg.imread(random_image_path)
  plt.imshow(img)
  plt.title(target_class)
  plt.axis(False);

## Function for comparing histories of model with and without fine-tuning:

def compare_histories(previous_history,new_history,initial_epochs = 5):

  ## getting un-tuned history data
  
  accuracy = previous_history.history["accuracy"]
  loss = previous_history.history["loss"]

  val_accuracy = previous_history.history["val_accuracy"]
  val_loss = previous_history.history["val_loss"]

  ## adding tuned history data

  total_accuracy = accuracy + new_history.history["accuracy"]
  total_loss = loss + new_history.history["loss"]

  total_val_accuracy = val_accuracy + new_history.history["val_accuracy"]
  total_val_loss = val_loss + new_history.history["val_loss"]

  ## Make plots:

  plt.figure(figsize=(8,8))
  plt.subplot(2,1,1)
  plt.plot(total_accuracy,label = "Training Accuracy")
  plt.plot(total_val_accuracy, label = "Validation Accuracy")
  plt.title("Training and Validation Accuracy")
  plt.legend(loc = "lower right")
  plt.axvline(x=initial_epochs-1,color = "green",ls = "--")


  plt.subplot(2, 1, 2)
  plt.plot(total_loss, label='Training Loss')
  plt.plot(total_val_loss, label='Validation Loss')
  plt.legend(loc='upper right')
  plt.title('Training and Validation Loss')
  plt.xlabel('epochs')
  plt.axvline(x = initial_epochs-1,color = "green",ls = "--")
  plt.show()

def predict_plot(model,filename,class_names):

  img = load_resize_image(filename)  ## loading and resizing image as per our model

  pred = model.predict(tf.expand_dims(img),axis = 0) ## make prediction after adjusting it's dimensions as per our model

  if len(pred[0]) > 1:
    pred_class = class_names[pred.argmax()]
  else:
    pred_class = class_names[int(tf.round(pred[0][0]))]

  plt.imshow(img)
  plt.title(f'Predicted class: {pred_class}')
  plt.axis(False);

