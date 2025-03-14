import os
import pandas as pd

from czerny import czerny, czerny_plot

set = int(input("ingresa el NUMERO del set. ej: 3 para images3, 2 para images2: \n"))


# Definir directorios
output_dir = f"./imagenes_curvas_{set}"
# Crear carpeta si no existe
os.makedirs(output_dir, exist_ok=True)


# sacamos los lc*data de nuestro filtrado
file_list_dir=f'../register{set}/phot.data'
data = pd.read_csv(file_list_dir, sep=' ', header=None)

file_list = data.iloc[:, 4].tolist()

# procesar cada curva de luz
for lc_i in file_list: 
    print(f"\n⚙️ Procesando {lc_i}...")
    
    # ejecutar czerny para cada lc#
    czerny(lc_file=lc_i, set=set)
    
    # guardar curvas
    czerny_plot(lc_num=lc_i, set=set)


print("\n🚀 Proceso completado. Las imagenes estan en:", output_dir)