#!/usr/bin/env python3

import glob
import time
import random
import os
from PIL import Image, ImageOps
from inky.auto import auto

inky = auto()

SATURATION = 0.5

PHOTO_PATH = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/images'
BORDER_COLOR = inky.WHITE
RESAMPLING = Image.BICUBIC

print('Reloading list of images')
photos = glob.glob(PHOTO_PATH + '/happy*')
random.shuffle(photos)
photo = photos[0]

print('Display {}'.format(photo))
image = Image.open(photo)
resizedimage = ImageOps.pad(image, inky.resolution, RESAMPLING, BORDER_COLOR)
inky.set_image(resizedimage, saturation=SATURATION)
inky.set_border(BORDER_COLOR)
inky.show()
