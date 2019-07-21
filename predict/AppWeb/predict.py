
import cv2
import numpy as np
from tensorflow.python.keras.models import *

import matplotlib.pyplot as plt
import os, time
from PIL import Image
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from flask import Flask, request, render_template, send_from_directory, flash, send_from_directory  # working with, mainly resizing, images
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing.image import img_to_array

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'jfif'])
IMG_SIZE = 48

# app = Flask(__name__)
# CORS(app)

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')

MODEL_PATH="C:\\Users\\mouad\\PycharmProjects\\Dice\\models\\"


from PIL import Image

def make_square(im, min_size=48, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


@app.route("/predict/<model>")
def predict(model):

    #load model
    model = load_model(MODEL_PATH+model)

    #load image
    test_image = Image.open("C:\\Users\\mouad\\Desktop\\hugo.jpg")
    new_image = make_square(test_image)
    new_image.save('temp.png')

    img = cv2.imread('temp.png')
    img = cv2.resize(img, (48, 48), interpolation = cv2.INTER_AREA)
    img = np.reshape(img, (-1, 6912)) / 255.0

    #predict model
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)
    classes = model.predict(img)
    answer = np.argmax(classes,axis=1)

    # image = Image.fromarray(classes, 'RGB')
    # image.save('my.png')
    # image.show()
    print(answer[0])
    #return qqch

    if answer[0] == 0:
        return str(4)
    if answer[0] == 1:
        return str(6)
    if answer[0] == 2:
        return str(8)
    if answer[0] == 3:
        return str(10)
    if answer[0] == 4:
        return str(12)
    if answer[0] == 5:
        return str(20)

    return 0


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'static')

        if not os.path.isdir(target):
            os.mkdir(target)

        model = request.files["model"]
        files = request.files.getlist("files")


        if files and model:
            modelname = model.filename
            filename = predict(files, modelname)

            return filename

        else:
            flash('No file part')
            return render_template('index.html')


@app.route('/send_image/<name>')
def send_image(name):
    image = send_from_directory("static", name)
    return image


def predict(files, model):

    # #load model
    # load_model("./models/"+model)
    #
    # #load image
    # img = cv2.imread(image_name)
    # img = cv2.resize(img, (48, 48), interpolation = cv2.INTER_AREA)
    # img = np.reshape(img, (-1, 6912)) / 255.0
    #
    # image_list = np.reshape(image_list, (14284, 6912)) / 255.0
    #
    # #predict model
    # classes = model.predict_classes(img)
    #
    #
    # #return qqch

    model = load_model(MODEL_PATH+model)
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)
    i = 0
    labels = []
    plt.figure(figsize=(48, 48), dpi=80)
    plt.xlabel('xlabel', fontsize=18)
    plt.ylabel('ylabel', fontsize=16)
    plt.axis("off")
    for file in files:
        image_read = cv2.imread("C:\\Users\\mouad\\Desktop\\54258050_p0.jpg")
        img = cv2.resize(image_read, (48, 48), interpolation=cv2.INTER_AREA)
        image = img
        image = Image.fromarray(image, 'RGB')
        img = np.reshape(img, (-1, 6912)) / 255.0

        # image = dataFromImage(file)
        # img = img_to_array(image)
        # img = np.expand_dims(image, axis=0)
        # image = Image.fromarray(image, 'RGB')
        # label = ''


        result = model.predict(test_datagen.flow(img, batch_size=1))

        # if result > 0.5:
        #     labels.append('dog')
        # else:
        #     labels.append('cat')

        if result < 1:
            labels.append('4')
        if result < 2 & result >1:
            labels.append('6')
        if result  < 3 & result >2:
            labels.append('8')
        if result < 4 & result >3:
            labels.append('10')
        if result < 5 & result >4:
            labels.append('12')
        if result >5:
            labels.append('20')

        plt.subplot(2, 2, i+1)
        plt.title('This is a ' + labels[i])
        imgplot = plt.imshow(image)
        i += 1

        if i % 10 == 0:
            break

    target = os.path.join(APP_ROOT, 'static')
    image_name = "plot" + str(time.time()) +".jpeg"
    finalUrl = "/".join([target, image_name])
    plt.savefig(finalUrl, bbox_inches="tight")

    return image_name


def dataFromImage(file):
    data = file.read()
    image = np.asarray(bytearray(data))
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))

    return image


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-\
    revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == "__main__":
    app.run()
