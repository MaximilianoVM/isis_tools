import pandas as pd
import glob
import re
import os

from process_methods import format_archives, calculate_offset, merge_by_date, instrumental_magnitude

DATA_DIR = str(input("DATA_DIR: ej. NGC_6426V \n"))
IMAGES_DIR = str(input("header_info_images????: ej. 6426V \n"))
header_file = f'{DATA_DIR}/header_info_images{IMAGES_DIR}'

DATE_FORMAT = str(input("JD o HJD \n"))

#pattern = re.compile(r"lc(\d+)\.data$")
pattern = re.compile(r"lc(\d+)(?:_(\d+))?\.data$") # para los MERGED


for file in glob.glob(f"{DATA_DIR}/lc*.data"):
    match = pattern.search(os.path.basename(file))
    if not match:
        continue  # skip archives w no number

    number = match.group(1)  # extract number
    print(f"Procesando {file}...")

    
    # PROCESSING
    header_info_df, lc_data_df = format_archives(header_file, file, DATE_FORMAT)
    #lc_data_df = calculate_offset(lc_data_df)
    merged_df = merge_by_date(lc_data_df, header_info_df, DATE_FORMAT)
    processed_df = instrumental_magnitude(merged_df)

    # DIRECTORIES
    output_dir = f"{DATA_DIR}/processed"
    output_path = f"{output_dir}/lc{number}_processed.data"
    # create dirs if not exist
    os.makedirs(output_dir, exist_ok=True)
    
    # order columns
    if "MagInstr" in processed_df.columns and "Flux" in processed_df.columns:
        cols = list(processed_df.columns)
        cols.remove("MagInstr")
        flujo_index = cols.index("Flux")
        cols.insert(flujo_index + 1, "MagInstr")
        processed_df = processed_df[cols]
        
    processed_df = processed_df.drop(['refFlux', 'errFlux', 'errRefF'], axis=1)

    # save w ordered columns
    processed_df.to_csv(output_path, sep='\t', index=False)
    print(f"✅ Archivo guardado como {output_path}\n")
    
    
