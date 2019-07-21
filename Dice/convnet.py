from tensorflow import keras
import numpy as np
import cv2
import matplotlib.pyplot as plt

from tensorflow.python.keras.activations import *
from tensorflow.python.keras.callbacks import *
from tensorflow.python.keras.datasets import *
from tensorflow.python.keras.layers import *
from tensorflow.python.keras.losses import *
from tensorflow.python.keras.models import *
from tensorflow.python.keras.optimizers import *
from tensorflow.python.keras.utils import *

import datetime

TRAIN_FOLDER = "dice10/train/"
TEST_FOLDER = "dice10/valid/"


def create_conv_net(output_activation_fct: int, nb_hidden_layers: int, categorical_nb: int):
    # input_layer = Input(shape=(6912,))
    # previous_layer = Reshape((48, 48, 3))(input_layer)
    #
    # for i in range(1, nb_hidden_layers+1):
    #     hidden_layer = Conv2D(2**3 * i, 6, padding="same", activation=relu )(previous_layer)
    #     pool_layer = MaxPool2D()(hidden_layer)
    #     previous_layer = pool_layer
    #
    # #first relu
    # # hidden_layer =Concatenate()([previous_layer, input_layer])
    # # pool_layer = MaxPool2D()(hidden_layer)
    # # previous_layer = pool_layer
    #
    # output_layer = Dense(categorical_nb, activation=output_activation_fct)(previous_layer)
    #
    # model =  Model(input_layer, output_layer)
    #
    # model.compile(loss=mse, optimizer=sgd(momentum=0.9), metrics=['accuracy'])
    # return model



    model = Sequential()
    model.add(Reshape((48, 48, 3), input_shape=(6912,)))
    model.add(Conv2D(16, 6, padding='same', activation=relu))
    model.add(AveragePooling2D())
    model.add(Conv2D(32, 6, padding='same', activation=relu))
    model.add(AveragePooling2D())
    model.add(Conv2D(64, 6, padding='same', activation=relu))
    model.add(AveragePooling2D())

    model.add(Flatten())

    model.add(Dense(6, activation=sigmoid))
    model.compile(loss=mse, optimizer=sgd(momentum=0.9), metrics=['accuracy'])
    return model




def switch_folder_test(dice_folder: int):

    if dice_folder == 4:
        return 0
    if dice_folder == 8:
        return 1
    if dice_folder == 6:
        return 2
    if dice_folder == 10:
        return 3
    if dice_folder == 12:
        return 4
    if dice_folder == 20:
        return 5

    return -1

if __name__ == "__main__":
    folder_list = []
    image_list = []

    # Preprocessing data
    part_of_test = ["d4", "d8", "d6", "d10", "d12", "d20"]
    for folder in part_of_test:
        for image in os.listdir(TRAIN_FOLDER + folder):
            image_read = cv2.imread(TRAIN_FOLDER + folder + "/" + image)
            image_list.append(image_read)
            folder_list.append(int(switch_folder_test(int(folder[1:]))))
    image_list = np.reshape(image_list, (-1, 6912)) / 255.0

    folder_test_list = []
    image_test_list = []

    for folder in part_of_test:
        for image in os.listdir(TEST_FOLDER + folder):
            image_test_read = cv2.imread(TEST_FOLDER + folder + "/" + image)
            image_test_list.append(image_test_read)
            folder_test_list.append(int(switch_folder_test(int(folder[1:]))))

    image_test_list = np.reshape(image_test_list, (-1, 6912)) / 255.0

    x_train = image_list
    y_train = folder_list
    x_test = image_test_list
    y_test = folder_test_list

    y_train = keras.utils.to_categorical(y_train, 6)
    y_test = keras.utils.to_categorical(y_test, 6)

    model = create_conv_net(sigmoid, 5, 6)

    model_name = "conv_6dices_" + datetime.datetime.now().strftime(
        "%Y_%m_%d_%H_%M_%S")

    tp_callback = TensorBoard("./log/" + model_name)

    print(model.summary())

    model.fit(x_train, y_train, epochs=200, batch_size=64, verbose=1,
              callbacks=[tp_callback], validation_data=(x_test, y_test))

    #plot_model(model, './models/' + model_name + '.png', show_shapes=True, show_layer_names=True)
    model.save('./models/' + model_name)
