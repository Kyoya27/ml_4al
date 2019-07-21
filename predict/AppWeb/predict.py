
import cv2
import numpy as np
from tensorflow.python.keras.models import *
import matplotlib.pyplot as plt
import os, time
from PIL import Image
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from flask import Flask, request, render_template, send_from_directory, flash, send_from_directory 
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing.image import img_to_array

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'jfif'])


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config.from_object('config')

MODEL_PATH="C:\\Users\\mouad\\PycharmProjects\\Dice\\models\\"
FILE_PATH="C:\\Users\\mouad\\Desktop\\"



def make_square(im, min_size=48, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


@app.route("/predict/<model>")
def predict(model, filename):

    #load model
    model = load_model(MODEL_PATH+model)

    #load image
    test_image = Image.open(FILE_PATH+filename)
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
            return predict(modelname, files[0].filename)

        else:
            flash('No file part')
            return render_template('index.html')


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
