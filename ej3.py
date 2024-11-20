import os
import numpy as np
from PIL import Image
from threading import Thread
from utils import get_path
import time

def thread_process(start_step, end_step, img1, img2, num_steps):
  for step in range(start_step, end_step + 1):
    P = step / num_steps
    result = (img1 * P + img2 * (1 - P)).astype(np.uint8)
    image = Image.fromarray(result)
    image.save(f"{path}/archives/shared/image-{step}.jpg")
    print(f"Imagen {step} generada, faltan {num_steps - step}")

start_time = time.time()
path = get_path()
num_threads = 4
num_steps = 96

# img1 = np.array(Image.open(f"{path}/images/image1.jpg").convert('RGB'), dtype=np.uint8)
# img2 = np.array(Image.open(f"{path}/images/image2.jpg").convert('RGB'), dtype=np.uint8)
img1 = np.array(Image.open(f"{path}/images/image1-800x800.jpg").convert('RGB'), dtype=np.uint8)
img2 = np.array(Image.open(f"{path}/images/image2-800x800.jpg").convert('RGB'), dtype=np.uint8)
# img1 = np.array(Image.open(f"{path}/images/image1-2000x2000.jpg").convert('RGB'), dtype=np.uint8)
# img2 = np.array(Image.open(f"{path}/images/image2-2000x2000.jpg").convert('RGB'), dtype=np.uint8)
# img1 = np.array(Image.open(f"{path}/images/image1-5000x5000.jpg").convert('RGB'), dtype=np.uint8)
# img2 = np.array(Image.open(f"{path}/images/image2-5000x5000.jpg").convert('RGB'), dtype=np.uint8)

if img1.shape != img2.shape:
    print("Las imágenes deben ser del mismo tamaño")
    exit()

steps_per_thread = num_steps // num_threads
threads = []

for i in range(num_threads):
    start_step = i * steps_per_thread
    end_step = (i + 1) * steps_per_thread if i < num_threads - 1 else num_steps

    thread = Thread(target=thread_process, args=(start_step, end_step, img1, img2, num_steps))
    threads.append(thread)
    thread.start()

for thread in threads:
    # Bloquea la ejecución del hilo principal hasta que el hilo especificado termine. Esto asegura que el hilo principal espere hasta que el hilo hijo termine antes de continuar.
    thread.join()

print(f"Imagenes guardadas en: {path}/archives/shared")

end_time = time.time()
total_time = end_time - start_time
print(f"Tiempo de ejecucion: {total_time:.6f} segundos")