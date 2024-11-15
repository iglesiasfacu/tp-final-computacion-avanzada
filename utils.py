import os
from datetime import datetime
from PIL import Image

# path del directorio actual
def get_path():
  return os.path.dirname(os.path.abspath(__file__))

# chequea que ambas imagenes tengan el mismo tamaño
def check_images_dimensions(img1, img2):
  return img1.size == img2.size