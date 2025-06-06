import pandas as pd
import numpy as np

header_file = 'header_info_images6426V'
data_file = 'lc44.data'
otuput_name = 'lc44_processed.data'


def format_archives(header_file, data_file, date_format): 
    # load data
    header_info = pd.read_csv(header_file, delim_whitespace=True, names=['file', 'JD', 'HJD', 'UT', 'EXPTIME', 'FILTER'])

    lc_data = pd.read_csv(data_file, delim_whitespace=True, names=[date_format, 'Flux', 'errFlux', 'refFlux', 'errRefF', 'calSNR'])

    # JD - 2460400
    header_info['JD'] = header_info['JD'] - 2460400
    header_info['HJD'] = header_info['HJD'] - 2460400
    
    return header_info, lc_data


def merge_by_date(lc_data, header_info, date_format): 
    merged_df = pd.merge_asof(
        lc_data.sort_values(by=date_format),                # DataFrame base
        header_info.sort_values(by=date_format),            # DataFrame to join
        on=date_format,               # key column
        direction='nearest',   # join w nearest HJD
        tolerance=0.0005
    )
    
    return merged_df

def instrumental_magnitude(lc_data): 
    # Flux to instrumental magnitude
    
    offset = calculate_offset(lc_data)
    
    lc_data['MagInstr'] = 25.0 - 2.5*np.log10(lc_data['Flux']+offset) + 2.5*np.log10(lc_data['EXPTIME'])
    return lc_data


def calculate_offset(lc_data):
    # calculate offset required to not handle negative values
    offset_obj = abs(lc_data['Flux'].min()) + 10
    offset_ref = abs(lc_data['refFlux'].min()) + 10

    offset = max(offset_obj, offset_ref)

    return offset






















