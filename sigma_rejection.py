import numpy as np
import pandas as pd


def sigma_rejection(df, column, num_sigma): 
    # Convertir la columna 'value' a un array de NumPy
    elements = np.array(df[column])

    # Calcular la media y la desviación estándar
    mean = np.mean(elements)
    sd = np.std(elements)

    # Filtrar el DataFrame
    filtered_df = df[
        (df[column] > mean - num_sigma * sd) & 
        (df[column] < mean + num_sigma * sd)
    ]
    
    return filtered_df