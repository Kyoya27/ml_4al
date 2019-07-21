from tensorflow.python.keras.models import *
from tensorflow.python.keras.activations import *
from tensorflow.python.keras.layers import *
from tensorflow.python.keras.losses import *
from tensorflow.python.keras.optimizers import *
from tensorflow.python.keras.utils import *
from tensorflow.python.keras.metrics import *
from tensorflow.python.keras.datasets import *
from tensorflow.python.keras.callbacks import *
import pydot_ng as pyd
import numpy as np
import tensorflow.python.keras as keras


keras.utils.vis_utils.pydot = pyd

def create_mlp(input_dim: int, hidden_layer_count: int, neurons_count_per_hidden_layer: int, output_dim):
    model = Sequential()

    for i in range(hidden_layer_count):
        if i == 0:
            model.add(Dense(neurons_count_per_hidden_layer, activation=tanh, input_dim=input_dim))
        else:
            model.add(Dense(neurons_count_per_hidden_layer,
                            activation=tanh))

    model.add(Dense(output_dim, activation=sigmoid))
    model.compile(optimizer=sgd(), loss=mse, metrics=["accuracy"])

    return model


if __name__ == "__main__":

    (x_train, y_train), (_, _) = mnist.load_data()

    small_x = x_train[:1000]
    small_y = y_train[:1000]

    print(small_x.shape)
    small_x = np.reshape(small_x, (1000, 28 * 28)) / 255.0

    small_y = keras.utils.to_categorical(small_y, 10)

    print(small_x.shape)

    for l in range(0, 5):
        for power_n in range(3, 10):
            if power_n > 3 and l == 0:
                break
            model = create_mlp(784, l, 2 ** power_n, 10)

            model_name = "Zmlp" + str(1) + "_" + str(2 ** power_n)

            tp_callback = TensorBoard("./log/" + model_name)

            model.fit(small_x, small_y,
                      epochs=1000,
                      batch_size=128,
                      validation_split=0.2, callbacks=[tp_callback])

            #plot_model(model, "./models/" + model_name + ".png", show_shapes=True, show_layer_names=True)
            model.save("./models/" + model_name)
