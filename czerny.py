import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def czerny(lc_file='lc0.data'): 
    lc_output = "lc.data"  # Archivo de salida esperado
    print(f"\n⚙️ Procesando {lc_file}...")

    # Ejecutar czerny y esperar a que termine
    czerny_command = f"../bin/czerny -i ../images3/{lc_file} -a 0.2 -n 1"
    result = subprocess.run(czerny_command, shell=True, capture_output=True, text=True)

    #coordenadas
    coords_data = pd.read_csv('../register3/phot.data', sep=' ', header=None)
    lc_data = coords_data[coords_data[4] == lc_file]
    lc_coords =  int(lc_data[2]), int(lc_data[3])
    #
    
    # Mostrar salida y errores de czerny
    print("🔍 Salida estandar de czerny:\n", result.stdout)
    if result.stderr:
        print("⚠️ Errores de czerny:\n", result.stderr)
        
        
    # ---------------------
    # Obtener la última línea del output
    output_lines = result.stdout.splitlines()
    if output_lines:
        last_line = output_lines[-1]
        print(f"📄 Última línea del output: {last_line}")

        # Guardar la última línea en un archivo
        with open("./outputs/last_line.txt", "w") as file:
            file.write(last_line + str(lc_coords) + "\n")  # Añadir un salto de línea al final
        print("✅ Última línea guardada en 'last_line.txt'")
    else:
        print("❌ No hay salida para procesar.")
    # ---------------

    # Esperar a que el archivo se genere
    if not os.path.exists(lc_output):
        print(f"❌ Error: No se genero {lc_output}")
        #continue  # Saltar al siguiente archivo
    
    
#czerny()

def czerny_plot(lc_num='#'): 
    lc_output='./lc.data' # datos a graficar
    output_dir = "./imagenes_curvas" # aqui se guardan
    last_line_file = "./outputs/last_line.txt"  # Archivo con la última línea
    
    # Leer la última línea del archivo
    try:
        with open(last_line_file, "r") as file:
            last_line = file.readline().strip()  # Leer y eliminar saltos de línea
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {last_line_file}")
        last_line = f"Curva de luz en fase ({lc_num})"  # Título por defecto

    # cargar datos 
    data = np.loadtxt(lc_output)
    phase = data[:, 0]  # 1ra columna: Fase
    flux = data[:, 1]   # 2da columna: Flujo

    # Generar grafica
    plt.figure(figsize=(8, 6))
    plt.scatter(phase, flux, s=10, color='magenta', label=f'Curva {lc_num}')
    plt.xlabel('Fase')
    plt.ylabel('Flujo')
    plt.title(last_line)
    plt.legend()
    plt.grid()
    
    # Guardar imagen
    save_path = os.path.join(output_dir, f"{lc_num}_P.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ Guardada: {save_path}")