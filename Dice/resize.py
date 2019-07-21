import os, sys
from PIL import Image
import io
from resizeimage import resizeimage


TRAIN_FOLDER = "dice2/train/"
TEST_FOLDER = "dice2/valid/"

part_of_test = ["d4", "d6", "d8", "d10", "d12", "d20"]

for folder in part_of_test:
    for image in os.listdir(TRAIN_FOLDER + folder):
        fd_img = open(TRAIN_FOLDER + folder + "/" + image, 'r+b')
        img = Image.open(fd_img)
        img = resizeimage.resize_thumbnail(img, [48, 48])
        img.save(TRAIN_FOLDER + folder + "/" + image, img.format)
        fd_img.close()


for folder in part_of_test:
    for image in os.listdir(TEST_FOLDER + folder):
        fd_img = open(TEST_FOLDER + folder + "/" + image, 'r+b')
        img = Image.open(fd_img)
        img = resizeimage.resize_thumbnail(img, [48, 48])
        img.save(TEST_FOLDER + folder + "/" + image, img.format)
        fd_img.close()