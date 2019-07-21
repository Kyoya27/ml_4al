from tensorflow import keras
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import *
from tensorflow.python.keras.activations import *
from tensorflow.python.keras.layers import *
from tensorflow.python.keras.losses import *
from tensorflow.python.keras.optimizers import *
from tensorflow.python.keras.utils import *
from tensorflow.python.keras.metrics import *
from tensorflow.python.keras.datasets import *
from tensorflow.python.keras.callbacks import *
import datetime

TRAIN_FOLDER = "dice10/train/"
TEST_FOLDER = "dice10/valid/"

#lineaire sur 6
#mlp plus simple
#mlp avec activation/metrics changé
#essaie overfit mlp, sinon convnet/resent
#equilibrage du modele


def create_mlp(input_dim: int, hidden_layer_count: int, neurons_count_per_hidden_layer: int, output_dim):
    model = Sequential()

    for i in range(hidden_layer_count):
        if i == 0:
            model.add(Dense(neurons_count_per_hidden_layer, activation=tanh, input_dim=input_dim))
        else:
            model.add(Dense(neurons_count_per_hidden_layer,
                            activation=tanh))

    model.add(Dense(output_dim, activation=sigmoid))
    model.compile(optimizer=sgd(), loss=categorical_crossentropy, metrics=["accuracy"])

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
            # image_reshaped = np.reshape(image_read, (1, 691200))/255.0
            image_list.append(image_read)
            folder_list.append(int(switch_folder_test(int(folder[1:]))))
    image_list = np.reshape(image_list, (14284, 6912)) / 255.0

    folder_test_list = []
    image_test_list = []

    for folder in part_of_test:
        for image in os.listdir(TEST_FOLDER + folder):
            image_test_read = cv2.imread(TEST_FOLDER + folder + "/" + image)
            # image_test_reshaped = np.reshape(image_test_read, (1, 691200))/255.0
            image_test_list.append(image_test_read)
            folder_test_list.append(int(switch_folder_test(int(folder[1:]))))

    for v in image_test_list:
        if v.shape != (48, 48, 3):
            print(v.shape)
    print("End loop")
    image_test_list = np.reshape(image_test_list, (2039, 6912)) / 255.0

    x_train = image_list
    y_train = folder_list
    x_test = image_test_list
    y_test = folder_test_list

    y_train = keras.utils.to_categorical(y_train, 6)
    y_test = keras.utils.to_categorical(y_test, 6)

    for l in range(0, 1):
        for power_n in [7]:
            model = create_mlp(6912, l, 2 ** power_n, 6)

            model_name = "slp_6_dices_(train_test_inv)" + str(l) + "_" + str(2 ** power_n) + "_" + datetime.datetime.now().strftime(
                "%Y_%m_%d_%H_%M_%S")

            tp_callback = TensorBoard("./log/" + model_name)


            model.fit(x_test, y_test,
                      epochs=200,
                      batch_size=64,
                      verbose=1,
                      validation_data=(x_train, y_train), callbacks=[tp_callback])

            #plot_model(model, "./models/" + model_name + ".png", show_shapes=True, show_layer_names=True)
            model.save("./models/" + model_name)