# -*- coding: utf-8 -*-
"""model3.0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w4jRwKrRZMpk4YbGOzJoTVy07Dn0KGSb

Importing Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np
import cv2
import os

"""Data Preprocessing"""

import os

parent_folder = 'face_age'

image_arrays = []

for age_folder in os.listdir(parent_folder):
    age_folder_path = os.path.join(parent_folder, age_folder)

    if os.path.isdir(age_folder_path):
        for filename in os.listdir(age_folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                image_path = os.path.join(age_folder_path, filename)

                img = cv2.imread(image_path)

                if img is not None:


                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    if int(age_folder)<=5:
                        image_arrays.append((img_gray,1))

                    elif int(age_folder)<=12:
                        image_arrays.append((img_gray,2))

                    elif int(age_folder)<=18:
                        image_arrays.append((img_gray,3))

                    elif int(age_folder)<=30:
                        image_arrays.append((img_gray,4))

                    elif int(age_folder)<=45:
                        image_arrays.append((img_gray,5))

                    elif int(age_folder)<=65:
                        image_arrays.append((img_gray,6))

                    elif int(age_folder)<=80:
                        image_arrays.append((img_gray,7))

                    else:
                        image_arrays.append((img_gray,8))

image_arrays[1]

from sklearn.model_selection import train_test_split

train_data, temp_data = train_test_split(image_arrays, test_size=0.3, random_state=43)

val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)

"""Separating Dependent and Independent variable"""

x_train = [item[0] for item in train_data]
y_train = [item[1] for item in train_data]

x_test = [item[0] for item in test_data]
y_test = [item[1] for item in test_data]

x_val = [item[0] for item in val_data]
y_val = [item[1] for item in val_data]

x_train[0]

y_train[0]

x_test[0]

len(x_train)

len(x_test)

len(x_val)

x_train[0].shape

"""Resizing images pixel"""

new_size = (100, 100)
resized_x_train = []

for image in x_train:
    resized_image = cv2.resize(image, new_size)
    resized_x_train.append(resized_image)


resized_x_train = np.array(resized_x_train)

print(resized_x_train.shape)

resized_x_test = []


for image in x_test:
    resized_image = cv2.resize(image, new_size)
    resized_x_test.append(resized_image)


resized_x_test = np.array(resized_x_test)

resized_x_val = []

for image in x_val:
    resized_image = cv2.resize(image, new_size)
    resized_x_val.append(resized_image)

resized_x_val = np.array(resized_x_val)

plt.matshow(resized_x_test[0])

plt.matshow(resized_x_train[0])

y_train[0]

"""Normalizing x_dataset"""

x_train_normalized = resized_x_train / 255.0
x_test_normalized = resized_x_test / 255.0
x_val_normalized = resized_x_val / 255.0

x_test_normalized[0]

x_test_normalized.shape

x_train_normalized.shape

"""Flattering X_dataset"""

X_train_flattened = x_train_normalized.reshape(len(x_train_normalized), 100*100)
X_test_flattened = x_test_normalized.reshape(len(x_test_normalized), 100*100)
X_val_flattened = x_val_normalized.reshape(len(x_val_normalized), 100*100)

X_train_flattened.shape

X_train_flattened[0]

X_train_flattened[0]

X_train_flattened = np.array(X_train_flattened)

"""Convert  labels to one-hot encoded format"""

x_train_np = np.array(x_train)
x_test_np = np.array(x_test)
x_val_np = np.array(x_val)
y_train_np = np.array(y_train)
y_test_np = np.array(y_test)
y_val_np = np.array(y_val)

num_classes = 9

from keras.utils import to_categorical
y_train_one_hot = to_categorical(y_train_np, num_classes=num_classes)
y_test_one_hot = to_categorical(y_test_np, num_classes=num_classes)
y_val_one_hot = to_categorical(y_val_np, num_classes=num_classes)

"""Reshaping x_dataset"""

x_train_reshaped = X_train_flattened.reshape(-1, 100, 100, 1)
x_val_reshaped = X_val_flattened.reshape(-1, 100, 100, 1)
x_test_reshaped = X_test_flattened.reshape(-1, 100, 100, 1)

"""CNN Architecture"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.regularizers import l2

model = Sequential([
    Conv2D(32, kernel_size=(3, 3), input_shape=(100, 100, 1), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(256, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(512, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(256, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(9, activation='softmax')
])
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

"""Model training"""

from tensorflow.keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(
    monitor='val_accuracy',
    patience=10,
    restore_best_weights=True
)

history = model.fit(
    x_train_reshaped,
    y_train_one_hot,
    epochs=100,batch_size=16,
    validation_data=(x_val_reshaped, y_val_one_hot),
    callbacks=[early_stopping]
)

"""Plotting Loss and Accuracy curves"""

train_loss = history.history['loss']
val_loss = history.history['val_loss']
train_acc = history.history['accuracy']
val_acc = history.history['val_accuracy']


plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(train_loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()


plt.subplot(1, 2, 2)
plt.plot(train_acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.show()

label_dtype = X_train_flattened.dtype
print("Label Data Type:", label_dtype)

"""Evaluation on test data"""

x_test_reshaped = x_test_reshaped.reshape(-1, 100, 100, 1)
y_predict = model.predict(x_test_reshaped,batch_size=16)
model.evaluate(x_test_reshaped, y_test_one_hot, batch_size=16)

"""Plotting confusion Matrix"""

y_predict_labels=[np.argmax(i) for i in y_predict]
cn=tf.math.confusion_matrix(labels=y_test_np,predictions=y_predict_labels)
import seaborn as sn
plt.figure(figsize=(15,15))
sn.heatmap(cn, annot=True, fmt='d')
plt.xlabel('pred')
plt.ylabel('true')

"""Saving the model"""

def predict_with_model(model, input_data):
    return model(input_data)
model.save("saved_model")

"""Loading Model"""

import tensorflow as tf
loaded_model = tf.keras.models.load_model("saved_model")

loaded_model.evaluate(x_test_reshaped, y_test_one_hot, batch_size=16)

"""Real life Testing

"""

image = cv2.imread('Sample image for Real time testing.jpg')

img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

resized_image = cv2.resize(img_gray, (100,100))
image_np = np.array(resized_image)

resized_image = np.reshape(image_np, (-1, 100, 100, 1))

img_normalized = resized_image/ 255.0

prediction=loaded_model.predict(img_normalized)
max_position = np.argmax(prediction)

print("YOUR AGE IS: ")

if(max_position==1):
    print("0-5")
elif(max_position==2):
    print("6-12")
elif(max_position==3):
    print("13-18")
elif(max_position==4):
    print("19-30")
elif(max_position==5):
    print("31-45")
elif(max_position==6):
    print("46-65")
elif(max_position==7):
    print("66-80")
else:
    print(">81")