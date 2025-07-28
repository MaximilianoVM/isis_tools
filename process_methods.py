import pandas as pd
import numpy as np


def format_archives(header_file, data_file, date_format): 
    # load data that came from images headers,  name columns
    header_info = headerfile_to_df(header_file)

    # load lightcurves data
    lc_data = raw_lc_to_df(data_file, date_format)

    # JD - 2460400
    header_info['JD'] = header_info['JD'] - 2460400
    header_info['HJD'] = header_info['HJD'] - 2460400
    
    return header_info, lc_data # return data as dataframes equal in date format

def headerfile_to_df(header_file): 
    header_info = pd.read_csv(header_file, delim_whitespace=True, names=['file', 'JD', 'HJD', 'UT', 'EXPTIME', 'FILTER'], index_col=False)
    return header_info

def raw_lc_to_df(data_file, date_format): 
    lc_data = pd.read_csv(data_file, delim_whitespace=True, names=[date_format, 'Flux', 'errFlux', 'refFlux', 'errRefF', 'calSNR'], index_col=False)
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
    
    offset = calculate_offset(lc_data)
    
    lc_data['MagInstr'] = 25.0 - 2.5*np.log10(lc_data['Flux']+offset) + 2.5*np.log10(lc_data['EXPTIME'])
    return lc_data


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
    y_axis = np.array(df[column]) 
    
    # apply mean or median 
    if method == 'mean': 
        value = np.mean(y_axis)
    else: 
        value = np.median(y_axis)
    
    # make mean/median zero
    if value < 0: 
        df[column] = df[column] + value
    elif value > 0: 
        df[column] = df[column] - value



















