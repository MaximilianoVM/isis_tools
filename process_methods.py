import pandas as pd
import numpy as np

header_file = 'header_info_images6426V'
data_file = 'lc44.data'
otuput_name = 'lc44_processed.data'


def format_archives(header_file, data_file, date_format='HJD'): 
    # cargamos archivos
    header_info = pd.read_csv(header_file, delim_whitespace=True, names=['file', 'JD', 'HJD', 'UT', 'EXPTIME', 'FILTER'])

    lc_data = pd.read_csv(data_file, delim_whitespace=True, names=[date_format, 'Flujo', 'errFlujo', 'refFlujo', 'errRefF', 'calSNR'])

    # JD - 2460400 en el header (se asume en el data)
    header_info['JD'] = header_info['JD'] - 2460400
    header_info['HJD'] = header_info['HJD'] - 2460400  # Si también quieres ajustar HJD
    
    return header_info, lc_data


def offset(lc_data):
    # calculamos el offset necesario para quitarnos negativos
    offset_obj = abs(lc_data['Flujo'].min()) + 10
    offset_ref = abs(lc_data['refFlujo'].min()) + 10

    # el maximo de los dos
    offset = max(offset_obj, offset_ref)
    print(offset)

    # aplicamos el offset 
    lc_data['Flujo'] = lc_data['Flujo'] + offset
    lc_data['refFlujo'] = lc_data['refFlujo'] + offset
    
    return lc_data


def merge_data(lc_data, header_info, date_format='HJD'): 
    merged_df = pd.merge_asof(
        lc_data.sort_values(by=date_format),                # DataFrame base
        header_info.sort_values(by=date_format),            # DataFrame a unir
        on=date_format,               # columna clave
        direction='nearest',   # unir con el HJD más cercano
        tolerance=0.0005       # tolerancia opcional para evitar errores si hay diferencias grandes
    )

    merged_df = merged_df.drop(['refFlujo', 'errFlujo', 'errRefF'], axis=1)
    
    return merged_df

def instrumental_magnitude(merged_df): 
    # Flujo a magnitud instrumental
    merged_df['MagInstr'] = 25.0 - 2.5*np.log10(merged_df['Flujo']) + 2.5*np.log10(merged_df['EXPTIME'])
    return merged_df























