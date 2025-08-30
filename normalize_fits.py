from astropy.io import fits
import numpy as np
import os
import fnmatch

def get_median(file_path):
    with fits.open(file_path) as hdu:
        data = hdu[0].data.astype(float)
        median = np.median(data)
        return median if median != 0 else None

def normalize_fits(file_path, target_median):
    with fits.open(file_path, mode='update') as hdu:
        data = hdu[0].data.astype(float)
        original_median = np.median(data)
        if original_median == 0:
            print(f"⚠️  Mediana cero en {file_path}, se omite.")
            return
        scaled_data = data / original_median * target_median
        hdu[0].data = scaled_data
        hdu.flush()

# Entrada del usuario
IMAGES_DIR = input("IMAGES_DIR (ej. 6426V): ")
DATA_DIR = os.path.join('..', 'images' + IMAGES_DIR)

# Paso 1: Recolectar medianas válidas
medians = []
file_list = []

for file in os.listdir(DATA_DIR):
    if fnmatch.fnmatch(file, '*.fit*'):
        path = os.path.join(DATA_DIR, file)
        med = get_median(path)
        if med:
            medians.append(med)
            file_list.append(file)

if not medians:
    print("❌ No se encontraron medianas válidas.")
    exit()

# Paso 2: Calcular mediana global
target_median = np.median(medians)
print(f"\n✅ Mediana global calculada: {target_median:.2f}")

# Paso 3: Normalizar archivos
for file in file_list:
    file_path = os.path.join(DATA_DIR, file)
    normalize_fits(file_path, target_median)
    print(f"✔️  Normalizado: {file}")

print("\n🎉 Proceso completado.")
