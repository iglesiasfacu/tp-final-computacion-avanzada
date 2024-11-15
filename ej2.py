from mpi4py import MPI
import numpy as np
from PIL import Image
from utils import get_path

comm = MPI.COMM_WORLD
task_id = comm.Get_rank()
task_size = comm.Get_size()
path = get_path()
num_steps = 96

if task_id == 0:
    img1 = np.array(Image.open(f"{path}/images/image1.jpg").convert('RGB'), dtype=np.uint8)
    img2 = np.array(Image.open(f"{path}/images/image2.jpg").convert('RGB'), dtype=np.uint8)

    if img1.shape != img2.shape:
        print('Las imágenes deben ser del mismo tamaño')
        exit()

    height, width, channels = img1.shape
    total_bytes = height * width * channels  # en bytes

    img1_bytes = img1.tobytes()
    img2_bytes = img2.tobytes()
else:
    total_bytes = None
    img1_bytes = None
    img2_bytes = None

total_bytes = comm.bcast(total_bytes, root=0)

img1_bytes_aux = bytearray(total_bytes)
img2_bytes_aux = bytearray(total_bytes)

comm.Scatterv([img1_bytes, total_bytes, None, MPI.BYTE], img1_bytes_aux, root=0)
comm.Scatterv([img2_bytes, total_bytes, None, MPI.BYTE], img2_bytes_aux, root=0)

img1_arr = np.frombuffer(img1_bytes_aux, dtype=np.uint8).reshape(-1, 3)
img2_arr = np.frombuffer(img2_bytes_aux, dtype=np.uint8).reshape(-1, 3)

for step in range(num_steps + 1):
    P = step / num_steps
    result_part = (img1_arr * P + img2_arr * (1 - P)).astype(np.uint8)

    result_bytes = None
    if task_id == 0:
        result_bytes = bytearray(total_bytes)
    else:
        result_bytes = None

    comm.Gatherv(result_part.tobytes(), [result_bytes, total_bytes, None, MPI.BYTE], root=0)

    if task_id == 0:
        result_img = np.frombuffer(result_bytes, dtype=np.uint8).reshape((height, width, channels))
        Image.fromarray(result_img).save(f"{path}/archives/distributed/image-{step}.jpg")
        print(f"Imagen {step} generada, faltan {num_steps - step}")
print(f"Imágenes guardadas en: {path}/archives/distributed")
