#!/bin/bash

# Definir las variables sets y todas
todas=($(awk '{print $1}' NGC6426/coordinates_NGC6426.dat))
sets=($(ls -d NGC6426_*))

echo "Sets encontrados: ${#sets[@]}"
echo "IDs encontrados: ${#todas[@]}"

# Crear directorios principales
mkdir -p NGC6426/lcs/I NGC6426/lcs/V

# Procesar cada set
for s in "${sets[@]}"; do
    echo "Procesando set: $s"
    
    # Procesar cada ID
    for id in "${todas[@]}"; do
        # Para archivos I - versión más eficiente
        files_i=$(find "${s}/lcs/" -maxdepth 1 -name "*I_${id}_mag.data" 2>/dev/null)
        if [ -n "$files_i" ]; then
            mkdir -p "NGC6426/lcs/I/${id}"
            echo "$files_i" | while read -r file; do
                mv "$file" "NGC6426/lcs/I/${id}/"
            done
        fi
        
        # Para archivos V - versión más eficiente
        files_v=$(find "${s}/lcs/" -maxdepth 1 -name "*V_${id}_mag.data" 2>/dev/null)
        if [ -n "$files_v" ]; then
            mkdir -p "NGC6426/lcs/V/${id}"
            echo "$files_v" | while read -r file; do
                mv "$file" "NGC6426/lcs/V/${id}/"
            done
        fi
    done
done

echo "Proceso completado!"