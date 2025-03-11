import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from lightcurve_plots import plot_save_lc

# Pedir el numero total de curvas de luz
#num_curves = int(input("Ingrese el numero total de curvas de luz a procesar: "))

# Definir directorios
#images3_dir = "../images3"
output_dir = "./imagenes_curvas"
# Crear carpeta si no existe
os.makedirs(output_dir, exist_ok=True)



# sacamos los lc*data de nuestro filtrado
#while list_file != 
#list_dir = input("Procesar: \n 1. lista filtrada \n 2. lista completa")
#file_list_dir='./outputs/filtered_phot.data'
file_list_dir='../register3/phot.data'
data = pd.read_csv(file_list_dir, sep=' ', header=None)

file_list = data.iloc[:, 4].tolist()

# procesar cada curva de luz
for lc_i in file_list: 
    print(f"\n⚙️ Procesando {lc_i}...")
    
    # guardar curvas
    #czerny_plot(lc_num=lc_i)
    plot_save_lc(lc_name=lc_i)


print("\n🚀 Proceso completado. Las imagenes estan en:", output_dir)