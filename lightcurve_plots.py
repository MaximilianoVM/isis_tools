import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

PUNTO = 2

# === PLOT EN FASE === 
# ojo con lc_path dependiendo de donde ejecutes czerny
def plot_phase(set='3'): 
    
    lc_path=f'../images{set}/lc.data'
    data = np.loadtxt(lc_path)
    
    # Separacion de columnas
    phase = data[:, 0]  # Primera columna: Fase
    flux = data[:, 1]   # Segunda columna: Flujo

    # Generar la grafica
    plt.figure(figsize=(8, 6))
    plt.scatter(phase, flux, s=PUNTO, color='blue', label='Curva de luz')
    plt.xlabel('Fase')
    plt.ylabel('Flujo')
    plt.title('Curva de luz en fase (lc#.data)')
    plt.legend()
    plt.grid()
    plt.show()

# === PLOT LC ESPECIFICA ===
def plot_lc(lc_path='../images3/lc0.data'): 
    # Carga de datos
    data = np.loadtxt(lc_path)
    jd = data[:, 0]
    values = data[:, 1]

    # Generar la grafica
    plt.figure(figsize=(8, 6))
    plt.scatter(jd, values, s=PUNTO, color='blue', label='Curva de luz')
    plt.xlabel('Fase')
    plt.ylabel('Flujo')
    plt.title('Curva de Luz (lc.data)')
    plt.legend()
    plt.grid()
    plt.show()
    
# === SAVE LC ESPECIFICA ===
def save_lc(lc_name='lc1.data', set=3, color='blue'): 
    output_dir = f"./imagenes_curvas_{set}" # aqui se guardan
    
    # Carga de datos
    data = np.loadtxt(f'../images{set}/{lc_name}')
    jd = data[:, 0] # fecha (JD)
    values = data[:, 1] # valores (que son?)

    # coordenadas
    coords_data = pd.read_csv(f'../register{set}/phot.data', sep=' ', header=None)
    lc_data = coords_data[coords_data[4] == lc_name]
    lc_coords =  int(lc_data[2]), int(lc_data[3])

    # Generar la grafica
    plt.figure(figsize=(8, 6))
    plt.scatter(jd, values, s=PUNTO, color=color, label='Curva de luz')
    plt.xlabel('JD')
    plt.ylabel('Value')
    plt.title(f'Curva de Luz ({lc_name}), coords:{lc_coords}')
    plt.legend()
    plt.grid()
    #plt.show()
    
    # Guardar imagen
    save_path = os.path.join(output_dir, f"{lc_name}.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ Guardada: {save_path}")


# === PLOT LCs EN GRUPO ===
def plot_lc_grouped(file_list_dir='./inputs/lc_list_group.data'): 
    # Directorio donde estan los archivos lc*.data
    directory ='../images3/'

    # Obtener lista de archivos lc*.data
    with open(file_list_dir, 'r') as f:
        file_list = f.read().splitlines()

    # Variables para almacenar datos combinados
    jd_combined = []
    values_combined = []

    # Cargar y combinar datos de todos los archivos
    for file_name in file_list:
        file_path = directory + file_name
        try:
            data = np.loadtxt(file_path)
            jd_combined.extend(data[:, 0])  # Primera columna (tiempo)
            values_combined.extend(data[:, 1])  # Segunda columna (flujo)
        except Exception as e:
            print(f"Error al cargar {file_name}: {e}")

    # Convertir listas a arreglos numpy
    jd_combined = np.array(jd_combined)
    values_combined = np.array(values_combined)

    # Generar la gráfica
    plt.figure(figsize=(10, 7))
    plt.scatter(jd_combined, values_combined, s=PUNTO, color='blue', label='Curva de luz combinada')
    plt.xlabel('Fase (JD)')
    plt.ylabel('Flujo')
    plt.title('Curva de Luz Combinada')
    plt.legend()
    plt.grid()
    plt.show()
