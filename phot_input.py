from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_coords(coords_path, reference_fit, wcs_file, output_name, output_dir, filtrar=False, show_id=False): 
    # Lee directamente en un array
    data = np.loadtxt(coords_path)

    # Cada columna en un array separado
    ids   = data[:,0].astype(int).astype(str)
    ras   = data[:,1]
    decs  = data[:,2]
    valor = data[:,3].astype(int)

    # world -> pixel (origin=1 para DS9 Physical)
    x_phys, y_phys = get_physical(wcs_file, ras, decs)

    hdr = fits.getheader(wcs_file)
    W = hdr.get('IMAGEW')   # 967 en tu header
    H = hdr.get('IMAGEH')   # 988 en tu header
    
    borde = 10

    if filtrar: 
        inside = (x_phys >= 0+borde) & (x_phys <= W-borde) & (y_phys >= 0+borde) & (y_phys <= H-borde)
        print("Dentro de imagen:", inside)
        x_phys = x_phys[inside]
        y_phys = y_phys[inside]
        ras = ras[inside]
        decs = decs[inside]
        ids = ids[inside]  # ¡Importante: también filtrar los IDs!
        valor = valor[inside]  # Y el valor también si lo necesitas
        
    df = phot_input_df(x_phys, y_phys, ras, decs, ids, valor)

    plot_coords(reference_fit, x_phys, y_phys, ids, save_path=output_dir+'/phot_'+output_name+'.png', show_id=show_id)
    
    # Guardar con el formato exacto
    df.iloc[:,:-3].to_csv(output_dir+'/phot_'+output_name+'.data', sep=' ', index=False, header=False, float_format='%.6f')
    
    return df

#### FUNCIONES AAAAA

def get_physical(wcs_file, ras, decs):
    # carga WCS generado por astrometry.net
    w = WCS(wcs_file)   # astropy detecta el header en el archivo

    # world -> pixel (origin=1 para DS9 Physical)
    x_phys, y_phys = w.all_world2pix(ras, decs, 1)   # arrays base-1 (DS9 physical)
    
    return x_phys, y_phys
    

def phot_input_df(x_phys, y_phys, ras, decs, ids, valor):
    # ORDEN Y FORMATO DE ARCHIVO PARA ISIS
    array_len = len(x_phys)
    # Crear el DataFrame con el formato específico
    df = pd.DataFrame({
        'x_phys': x_phys, 
        'y_phys': y_phys,
        'x_int': np.round(x_phys).astype(int),  # Redondear y convertir a entero
        'y_int': np.round(y_phys).astype(int),  # Redondear y convertir a entero
        'id': np.array(['lc' + str(id_num) + '.data' for id_num in ids]),
        'var_1': np.ones(array_len).astype(int), 
        'var_2': np.full(array_len, 7),
        'ras': ras, 
        'decs': decs, 
        'valor': valor
    })
    
    return df


    
def plot_coords(reference_fit, x_phys, y_phys, ids, save_path='imagen.png', show_id=False): 
    # lee imagen con datos
    img = fits.getdata(reference_fit)   # tu imagen con pixeles
    hdr_img = fits.getheader(reference_fit)

    # Convertir x_phys (base-1, DS9 physical) a índices de numpy (col,row) base-0:
    x0 = np.asarray(x_phys, float) - 1.0   # columnas (x) base-0
    y0 = np.asarray(y_phys, float) - 1.0   # filas (y) base-0

    plt.figure(figsize=(7,7))
    plt.imshow(img, origin='lower', cmap='gray', vmin=np.percentile(img,5), vmax=np.percentile(img,99))
    plt.scatter(x0, y0, s=0.7, color='red')
    
    if show_id:
        for i, (xx, yy, obj_id) in enumerate(zip(x0, y0, ids)):
            plt.text(xx+5, yy+5, str(obj_id), color='yellow', fontsize=5)
            
    plt.title('Overlay: puntos WCS sobre imagen')
    plt.xlabel('x (columnas, base-0)')
    plt.ylabel('y (filas, base-0)')
    plt.tight_layout()
    
    # GUARDAR LA IMAGEN SI SE PROPORCIONA UN PATH
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='black')
        print(f"Imagen guardada en: {save_path}")
    
    plt.show()

