import pandas as pd
import numpy as np


def format_archives(headerfile_path, lc_data_path, date_format): 
    # load data that came from images headers,  name columns
    header_info = headerfile_to_df(headerfile_path)

    # load lightcurves data
    lc_data = raw_lc_to_df(lc_data_path, date_format)

    # JD - 2460400
    header_info['JD'] = header_info['JD'] - 2460400
    header_info['HJD'] = header_info['HJD'] - 2460400
    
    return header_info, lc_data # return data as dataframes equal in date format

def headerfile_to_df(headerfile_path): 
    header_info = pd.read_csv(headerfile_path, delim_whitespace=True, names=['file', 'JD', 'HJD', 'UT', 'EXPTIME', 'FILTER'], index_col=False)
    return header_info

def raw_lc_to_df(lc_data_path, date_format='HJD'): 
    lc_data = pd.read_csv(lc_data_path, delim_whitespace=True, names=[date_format, 'Flux', 'errFlux', 'refFlux', 'errRefF', 'calSNR'], index_col=False)
    return lc_data


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
    df_w_instrumental = lc_data.copy()
    
    offset = calculate_offset(df_w_instrumental)
    
    df_w_instrumental['MagInstr'] = 25.0 - 2.5*np.log10(df_w_instrumental['Flux']+offset) + 2.5*np.log10(df_w_instrumental['EXPTIME'])
    return df_w_instrumental


def calculate_offset(lc_data):
    # calculate offset required to not handle negative values
    offset_obj = abs(lc_data['Flux'].min()) + 10
    offset_ref = abs(lc_data['refFlux'].min()) + 10

    offset = max(offset_obj, offset_ref)

    return offset


# ===== Julio 2025 =====

def sigma_rejection(df, column, num_sigma): 
    # make column an numpy array
    elements = np.array(df[column])

    # get median and standard deviation
    mean = np.mean(elements)
    sd = np.std(elements)

    # filter DataFrame
    filtered_df = df[
        (df[column] > mean - num_sigma * sd) & 
        (df[column] < mean + num_sigma * sd)
    ]
    
    return filtered_df

def zero_point_align(df, method='median', column='Flux'): # method = ['mean', 'median']
    df_aligned = df.copy()
    y_axis = np.array(df[column]) 
    
    # apply mean or median 
    if method == 'mean': 
        value = np.mean(y_axis)
    else: 
        value = np.median(y_axis)
        
    # make mean/median zero
    
    new_column = 'aligned_'+str(column)
    
    if value < 0: 
        df_aligned[new_column] = df_aligned[column] + value
    elif value > 0: 
        df_aligned[new_column] = df_aligned[column] - value
                
    return df_aligned



















