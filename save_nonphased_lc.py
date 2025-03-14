import os
import pandas as pd

from lightcurve_plots import plot_save_lc

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
    
    # guardar curvas
    plot_save_lc(lc_name=lc_i)


print("\n🚀 Proceso completado. Las imagenes estan en:", output_dir)