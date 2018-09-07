import sys
import os
import numpy as np
from keras.models import Sequential, model_from_json
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator

def train(input_dir,npy_file) :
    nb_classes = len([name for name in os.listdir(input_dir) if name != ".DS_Store"])
    x_train, x_test, y_train, y_test = np.load(npy_file)
    x_train = x_train.astype("float") / 255.
    x_test = x_test.astype("float") / 255.
    y_train = np_utils.to_categorical(y_train, nb_classes)
    y_test = np_utils.to_categorical(y_test, nb_classes)
    train_datagen = ImageDataGenerator(   #画像回転、ズームなどで水増し...
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest')

    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]))
    model.add(Activation('relu'))

    model.add(Conv2D(32, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(512))

    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    # 学習してベストモデルを保存
    checkpoint_cb = ModelCheckpoint("snapshot/cat-bestmodel.hdf5", save_best_only=True)
    result = model.fit_generator(train_datagen.flow(x_train,  y_train,
                    batch_size=64, save_to_dir=None),
                    epochs=50,
                    steps_per_epoch=None,
                    validation_data=(x_test, y_test),
                    validation_steps=None,
                    workers=4,
                    callbacks=[checkpoint_cb])

    # ベストモデルのテスト
    model.load_weights("snapshot/cat-bestmodel.hdf5")
    score = model.evaluate(x_test, y_test)
    print('loss=', score[0])
    print('accuracy=', score[1])

if __name__ == "__main__":
  args = sys.argv
  input_dir = args[1]
  npy_file = args[2]  #data.pyで保存したcat_color.npy
  train(input_dir, npy_file)
