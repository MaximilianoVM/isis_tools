import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


from lightcurve_plots import save_lc

# ================== Funciones ================
from astropy.timeseries import LombScargle
import numpy as np

# Usamos los valores de tiempo y flujo
#time = lc_data['HJD'].values
#flux = lc_data['Flux'].values

PUNTO = 4
def save_lomb_scargle(lc_name='lc1.data', set=3, color='green'): 
    output_dir = f"./imagenes_curvas_{set}" # aqui se guardan
    
    # Carga de datos
    data = np.loadtxt(f'../images{set}/{lc_name}')
    jd = data[:, 0] # fecha (JD)
    values = data[:, 1] # valores (que son?)

    # Calculamos el periodograma ====================
    frequency, power = LombScargle(jd, values).autopower()

    # Obtenemos el periodo con la potencia más alta
    best_period = 1 / frequency[np.argmax(power)]
    print(f"🌀 Mejor periodo estimado: {best_period:.6f} días")

    phased_time = (jd % best_period)
    # xxxxxxxxxxxxxxxxxxxxxxxxxx ====================

    # coordenadas
    coords_data = pd.read_csv(f'../register{set}/phot.data', sep=' ', header=None)
    lc_data = coords_data[coords_data[4] == lc_name]
    lc_coords =  int(lc_data[2]), int(lc_data[3])

    # Generar la grafica
    plt.figure(figsize=(8, 6))
    plt.scatter(phased_time, values, s=PUNTO, color=color, label='Curva de luz')
    plt.xlabel('JD')
    plt.ylabel('Value')
    plt.title(f'Curva de Luz ({lc_name}), coords:{lc_coords}')
    plt.legend()
    plt.grid()
    #plt.show()
    
    # Guardar imagen
    save_path = os.path.join(output_dir, f"{lc_name}_LS.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ Guardada: {save_path}")


    
# ================== Implementacion ================


set = str(input("ingresa el NUMERO del set. 🗃️ ej: 3 para images3, 2 para images2: \n"))
#color = str(input("ingresa el color para tus curvas \n ej. red 🔴, magenta 🟣, green 🟢, blue 🔵"))
color = 'black'

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
    save_lomb_scargle(lc_name=lc_i, set=set, color=color)


print("\n🚀 Proceso completado. Las imagenes estan en:", output_dir)