import os
import numpy as np
from PIL import Image
from utils import get_path
import time

start_time = time.time()
path = get_path()

# Cargar imágenes y convertirlas a matrices NumPy
# img1 = np.array(Image.open(f"{path}/images/image1.jpg").convert('RGB'), dtype=np.uint8)
# img2 = np.array(Image.open(f"{path}/images/image2.jpg").convert('RGB'), dtype=np.uint8)
img1 = np.array(Image.open(f"{path}/images/image1-800x800.jpg").convert('RGB'), dtype=np.uint8)
img2 = np.array(Image.open(f"{path}/images/image2-800x800.jpg").convert('RGB'), dtype=np.uint8)
# img1 = np.array(Image.open(f"{path}/images/image1-2000x2000.jpg").convert('RGB'), dtype=np.uint8)
# img2 = np.array(Image.open(f"{path}/images/image2-2000x2000.jpg").convert('RGB'), dtype=np.uint8)
# img1 = np.array(Image.open(f"{path}/images/image1-5000x5000.jpg").convert('RGB'), dtype=np.uint8)
# img2 = np.array(Image.open(f"{path}/images/image2-5000x5000.jpg").convert('RGB'), dtype=np.uint8)

num_steps = 96

if img1.shape != img2.shape:
    print("Las imágenes deben ser del mismo tamaño")
    exit()

height, width, channels = img1.shape
images = []

for step in range(num_steps + 1):
    P = step / num_steps
    result_img = (img1 * P + img2 * (1 - P)).astype(np.uint8)
    images.append(Image.fromarray(result_img))
    print(f"Imagen {step} generada, faltan {num_steps - step}")

# Guardar imágenes
output_dir = os.path.join(path, "archives", "sequential")
os.makedirs(output_dir, exist_ok=True)

for pos, img in enumerate(images):
    img.save(f"{output_dir}/image-{pos}.jpg")

print(f"Imágenes guardadas en: {output_dir}")

end_time = time.time()
total_time = end_time - start_time
print(f"Tiempo de ejecución: {total_time:.6f} segundos")
