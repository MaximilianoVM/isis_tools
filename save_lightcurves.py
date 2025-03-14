import os
import pandas as pd

from czerny import czerny, czerny_plot

# Definir directorios
output_dir = "./imagenes_curvas"
# Crear carpeta si no existe
os.makedirs(output_dir, exist_ok=True)


# sacamos los lc*data de nuestro filtrado
file_list_dir='../register3/phot.data'
data = pd.read_csv(file_list_dir, sep=' ', header=None)

file_list = data.iloc[:, 4].tolist()

# procesar cada curva de luz
for lc_i in file_list: 
    print(f"\n⚙️ Procesando {lc_i}...")
    
    # ejecutar czerny para cada lc#
    czerny(lc_file=lc_i)
    
    # guardar curvas
    czerny_plot(lc_num=lc_i)


print("\n🚀 Proceso completado. Las imagenes estan en:", output_dir)