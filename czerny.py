import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def czerny(lc_file='lc0.data'): 
    lc_output = "lc.data"  # Archivo de salida esperado
    print(f"\n⚙️ Procesando {lc_file}...")

    # Ejecutar czerny y esperar a que termine
    czerny_command = f"../bin/czerny -i ../images3/{lc_file} -a 0.2 -n 1"
    result = subprocess.run(czerny_command, shell=True, capture_output=True, text=True)

    # Mostrar salida y errores de czerny
    print("🔍 Salida estandar de czerny:\n", result.stdout)
    if result.stderr:
        print("⚠️ Errores de czerny:\n", result.stderr)

    # Esperar a que el archivo se genere
    if not os.path.exists(lc_output):
        print(f"❌ Error: No se genero {lc_output}")
        #continue  # Saltar al siguiente archivo
    
    
#czerny()

def czerny_plot(lc_num='#'): 
    lc_output='./lc.data'
    output_dir = "./imagenes_curvas"

    data = np.loadtxt(lc_output)
    phase = data[:, 0]  # 1ra columna: Fase
    flux = data[:, 1]   # 2da columna: Flujo

    # Generar grafica
    plt.figure(figsize=(8, 6))
    plt.scatter(phase, flux, s=10, color='blue', label=f'Curva {lc_num}')
    plt.xlabel('Fase')
    plt.ylabel('Flujo')
    plt.title(f'Curva de luz en fase ({lc_num})')
    plt.legend()
    plt.grid()
    
    # Guardar imagen
    save_path = os.path.join(output_dir, f"{lc_num}.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ Guardada: {save_path}")