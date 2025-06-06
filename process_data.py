import pandas as pd
import glob
import re
import os

from process_methods import format_archives, offset, merge_data, instrumental_magnitude

DATA_DIR = str(input("DATA_DIR: ej. NGC_6426V \n"))
IMAGES_DIR = str(input("IMAGES_DIR: ej. 6426V \n"))
header_file = f'{DATA_DIR}/header_info_images{IMAGES_DIR}'

pattern = re.compile(r"lc(\d+)\.data$")

for file in glob.glob(f"{DATA_DIR}/lc*.data"):
    match = pattern.search(os.path.basename(file))
    if not match:
        continue  # saltar archivos que no tienen número

    number = match.group(1)  # extrae el número
    print(f"Procesando {file}...")

    
    # datos a dataframes y asignamos nombres de columnas
    header_info_df, lc_data_df = format_archives(header_file, file)
    # aplicamos offset para el posterior paso de magnitudes
    lc_data_df = offset(lc_data_df)
    # asignamos sus headers a los datos para mejor manejo en un solo df
    merged_df = merge_data(lc_data_df, header_info_df)
    # pasamos el flujo a magnitud instrumental 
    instrumental_magnitude(merged_df)

    output_path = f"{DATA_DIR}/lc{number}_processed.data"
    merged_df.to_csv(output_path, sep='\t', index=False)
    print(f"✅ Archivo guardado como {output_path}\n")
    
    
