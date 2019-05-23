#!/usr/bin/env python

import time
import sys
import json

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageSequence, GifImagePlugin

# Matrix size
size = 256, 96

# Open source
if len(sys.argv) < 2:
  sys.exit("Require an image argument")
else :
  image_file = sys.argv[1]

im = Image.open(image_file)

# Get gif frames
frames = ImageSequence.Iterator(im)
frames_count = 0
print(im.info)
# Resize gif frames to matrix
def thumbnails(frames):
  for frame in frames:
      thumbnail = frame.copy()
      thumbnail.thumbnail(size, Image.ANTIALIAS)
      global frames_count
      frames_count += 1
      yield thumbnail

frames = thumbnails(frames)

# Save output
om = next(frames)# Handle first frame separately
om.info = im.info# Copy sequence info
om.save("out.gif", save_all = True, append_images = list(frames))
print(om.info)
# Pull back in resized gif
# image = Image.open("out.gif")
image = im

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 4
options.parallel = 3
#options.led_slowdown_gpio = 2
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Loop through gif frames and display on matrix.
fps = (round(frames_count,3) / image.info['duration']) * 10
print(fps)
while True:
  for frame in range(0, frames_count):
 #     print(image.n_frames)
      image.seek(frame)
      matrix.SetImage(image.convert('RGB'))
      time.sleep(fps)

# Handle quiting
try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
