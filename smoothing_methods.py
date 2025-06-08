import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_lc(x, y):
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, s=2.5, color='blue', label='Curva de luz')
    plt.xlabel('time')
    plt.ylabel('flux')
    plt.title('Curva de luz')
    plt.legend()
    plt.grid()
    plt.show()
    
    
    
def plot_subset(x_column, y_column, lc_data, subset): 
    plt.figure(figsize=(8, 6))

    # all points
    plt.scatter(lc_data[x_column], lc_data[y_column], label="All", color="gray", alpha=0.6)
    # Subset
    plt.scatter(subset[x_column], subset[y_column], label="subset data", color="red", edgecolor="black")

    plt.title(f"{x_column} vs {y_column}" )
    plt.xlabel(f"{x_column}")
    plt.ylabel(f"{y_column}")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    
    
def smooth_lc(lc_data, threshold, plot=True): 
    # sort by phase
    lc_sorted = lc_data.sort_values(by='Phased')

    # smooth by median
    smooth_flux = lc_sorted['Flux'].rolling(window=25, center=True).median()

    # compute residuals
    residuals = lc_sorted['Flux'] - smooth_flux

    # delete outliers by distance
    mask = residuals.abs() < threshold
    lc_clean = lc_sorted[mask]
    
    if plot:
        fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

        # Plot 1: original + smoothed
        axs[0].plot(lc_sorted['Phased'], lc_sorted['Flux'], '.', label='Curva original', alpha=0.5)
        axs[0].plot(lc_sorted['Phased'], smooth_flux, '-', color='red', linewidth=2, label='Curva suavizada')
        axs[0].set_title('Curva original y suavizada')
        axs[0].set_xlabel('Fase')
        axs[0].set_ylabel('Flujo')
        axs[0].legend()
        axs[0].grid(True)

        # Gráfico 2: Curva limpia
        axs[1].plot(lc_clean['Phased'], lc_clean['Flux'], '.', label='Curva limpia', color='blue')
        axs[1].set_title('Curva de luz limpia')
        axs[1].set_xlabel('Fase')
        axs[1].legend()
        axs[1].grid(True)

        plt.tight_layout()
        plt.show()
    
    return lc_clean


def shift_phase(lc_data, shift_amount):
    lc_data = lc_data.copy()
    lc_data['Phased'] = (lc_data['Phased'] - shift_amount) % 1
    return lc_data