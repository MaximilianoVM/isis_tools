import os
import pandas as pd

from lightcurve_plots import save_lc


set = str(input("ingresa el NUMERO del set. 🗃️ ej: 3 para images3, 2 para images2: \n"))
#color = str(input("ingresa el color para tus curvas \n ej. red 🔴, magenta 🟣, green 🟢, blue 🔵"))
color = 'blue'

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
    
    # guardar curvas
    save_lc(lc_name=lc_i, set=set, color=color)


print("\n🚀 Proceso completado. Las imagenes estan en:", output_dir)