import os
from PIL import Image
from utils import get_path

path = get_path()
img1 = Image.open(f"{path}/images/image1.jpg")
img2 = Image.open(f"{path}/images/image2.jpg")
num_steps = 5

if img1.size != img2.size:
    print('Las imágenes deben ser del mismo tamaño')
    exit()

images = []
for step in range(num_steps + 1):
    result = Image.new("RGB", img1.size)
    P = step / num_steps

    for i in range(result.width):
      for j in range(result.height):
        r = int(img1.getpixel((i, j))[0] * P + img2.getpixel((i, j))[0] * (1 - P))
        g = int(img1.getpixel((i, j))[1] * P + img2.getpixel((i, j))[1] * (1 - P))
        b = int(img1.getpixel((i, j))[2] * P + img2.getpixel((i, j))[2] * (1 - P))
        result.putpixel((i, j), (r, g, b))
    print(f"Imagen {step} generada, faltan {num_steps - step}")
    images.append(result)

for pos in range(len(images)):
    images[pos].save(f"{path}/archives/sequential/image-{pos}.jpg")
print(f"Imagenes guardadas en: {path}/archives/sequential")
