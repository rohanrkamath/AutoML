from flask import Flask, render_template, request, redirect, flash, url_for, session, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
# from myproject import db, app
from werkzeug.utils import secure_filename
from datetime import datetime
import time
import cv2

from backend.models import VGG_AE
from backend.metrics import vgg_perceptual_mse_loss
from backend.utils import create_dataset, create_validation_set, fixed_generator, calculate_threshold

import os
from pathlib import Path
import argparse
import shutil
import pandas as pd

from keras.applications.vgg16 import VGG16
from keras.optimizers import RMSprop, Adam
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, CSVLogger
from keras.preprocessing.image import ImageDataGenerator

from flask_login import login_user, current_user, logout_user, login_required
from glob import glob

from myproject.models import User, Project

IMAGE_SIZE = 224
CHANNELS = 3
BATCH_SIZE = 16
# EPOCHS = 15

AUGMENTATIONS = True
FPS = 10
VALIDATION_SPLIT = 0.2
REDUCE_LR_PATIENCE = 5
LOSS_WEIGHTS = [1.0, 0.25]

def train_test(epoch, input_videos_path, checkpoints_path):

    input_folder_path = input_videos_path
    model_save_path = checkpoints_path

    print(input_folder_path)

    input_frames_path = os.path.join(input_folder_path, "training_frames")
    input_frames_path_ok = os.path.join(input_frames_path, "OK")
    validation_frames_path = os.path.join(
        input_folder_path, "validation_frames")
    validation_frames_path_ok = os.path.join(validation_frames_path, "OK")

    if os.path.exists(input_frames_path):
        shutil.rmtree(input_frames_path)
    if os.path.exists(validation_frames_path):
        shutil.rmtree(validation_frames_path)

    Path(input_frames_path).mkdir(parents=True, exist_ok=True)
    Path(validation_frames_path).mkdir(parents=True, exist_ok=True)

    Path(input_frames_path_ok).mkdir(parents=True, exist_ok=True)
    Path(validation_frames_path_ok).mkdir(parents=True, exist_ok=True)

    create_dataset(videos_dir=input_folder_path,
                   output_dir=input_frames_path_ok,
                   fps=FPS)

    create_validation_set(input_frames_path_ok,
                          validation_frames_path_ok,
                          validation_split=VALIDATION_SPLIT,
                          method="last")

    # error
    loss_model = VGG16(include_top=False)
    model = VGG_AE(input_shape=(
        IMAGE_SIZE, IMAGE_SIZE, CHANNELS)).create_model()
    model.compile(loss=vgg_perceptual_mse_loss(
        loss_model, weights=LOSS_WEIGHTS), optimizer=Adam())
    print(model.summary())

    train_size = int(len(os.listdir(input_frames_path_ok)))
    valid_size = int(len(os.listdir(validation_frames_path_ok)))

    print("TRAIN SET SIZE: ", train_size)
    print("VALID SET SIZE: ", valid_size)

    if AUGMENTATIONS:
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            brightness_range=[0.95, 1.05],
            zoom_range=0.05,
            width_shift_range=0.05,
            height_shift_range=0.05,
            shear_range=0.05,
            fill_mode="nearest")
    else:
        train_datagen = ImageDataGenerator(rescale=1./255)

    valid_dataget = ImageDataGenerator(rescale=1./255)

    if CHANNELS == 3:
        color_mode = "rgb"
    elif CHANNELS == 1:
        color_mode = "grayscale"
    else:
        color_mode = "INVALID CHANNELS"

    train_generator = train_datagen.flow_from_directory(
        input_frames_path,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        color_mode=color_mode,
        batch_size=BATCH_SIZE,
        class_mode=None,
        shuffle=True)

    validation_generator = train_datagen.flow_from_directory(
        validation_frames_path,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        color_mode=color_mode,
        batch_size=BATCH_SIZE,
        class_mode=None,
        shuffle=True)

    checkpoint_save_path = os.path.join(model_save_path, 'model.h5')
    checkpoint = ModelCheckpoint(
        checkpoint_save_path, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    reduce_lr = ReduceLROnPlateau(
        'val_loss', factor=0.1, patience=REDUCE_LR_PATIENCE, verbose=1)
    csv_logger = CSVLogger(os.path.join(input_folder_path, "training_log.csv"))
    callbacks = [checkpoint, reduce_lr, csv_logger]
    # callbacks = [checkpoint, reduce_lr]

    history = model.fit_generator(fixed_generator(train_generator),
                                  steps_per_epoch=train_size // BATCH_SIZE,
                                  epochs=epoch,
                                  validation_data=fixed_generator(
        validation_generator),
        validation_steps=valid_size // BATCH_SIZE,
        callbacks=callbacks
    )

    model = VGG_AE(input_shape=(
        IMAGE_SIZE, IMAGE_SIZE, CHANNELS)).create_model()
    model.load_weights(os.path.join(model_save_path, 'model.h5'))
    losses, max_loss, min_loss, average_loss = calculate_threshold(
        model, validation_frames_path_ok)

    print("MAX_LOSS: ", max_loss)
    print("MIN_LOSS: ", min_loss)
    print("AVG_LOSS: ", average_loss)

    losses_df = pd.DataFrame(losses)
    losses_df.to_csv("losses.csv")