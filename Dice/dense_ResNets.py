from tensorflow import keras
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tensorflow.python.keras.datasets import *
from tensorflow.python.keras.activations import *
from tensorflow.python.keras.optimizers import *
from tensorflow.python.keras.losses import *
from tensorflow.python.keras.layers import *
from tensorflow.python.keras.models import *
from tensorflow.python.keras.callbacks import *
from tensorflow.python.keras.utils import *

import datetime

TRAIN_FOLDER = "dice10/train/"
TEST_FOLDER = "dice10/valid/"


def create_res_net(output_activation_fct: int, nb_hidden_layers: int, categorical_nb: int):

    input_tensor = Input((6912,))

    rslt_prev = input_tensor
    rslt_concat = input_tensor

    for i in range(nb_hidden_layers):
        rslt_bn = BatchNormalization()(rslt_concat)
        rslt_dense = Dense(32, activation=linear)(rslt_bn)
        rslt_activation = LeakyReLU()(rslt_dense)
        rslt_concat = Concatenate()([rslt_activation, rslt_prev])
        rslt_prev = rslt_activation

    rslt_bn = BatchNormalization()(rslt_concat)
    rslt = Dense(categorical_nb, activation=output_activation_fct)(rslt_bn)

    model = Model([input_tensor], [rslt])

    model.compile(loss=categorical_crossentropy, optimizer=adam(), metrics=['accuracy'])
    return model


def switch_folder_test(dice_folder: int):

    if dice_folder == 4:
        return 0
    if dice_folder == 6:
        return 1
    if dice_folder == 8:
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

    model = create_res_net(softmax, 20, 6)

    model_name = "res_net__6dices_" + datetime.datetime.now().strftime(
        "%Y_%m_%d_%H_%M_%S")

    tp_callback = TensorBoard("./log/" + model_name)

    print(model.summary())

    model.fit(x_train, y_train, epochs=200, batch_size=64,
              callbacks=[tp_callback], validation_data=(x_test, y_test))

    #plot_model(model, './models/' + model_name + '.png', show_shapes=True,show_layer_names=True)
    model.save('./models/' + model_name)
