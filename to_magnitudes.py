import numpy as np

def get_physical_by_id(physical_coords_file, star_id): 
    # Leer solo las columnas necesarias
    data = np.loadtxt(physical_coords_file, dtype=str)

    # Encontrar la fila para star_id
    for row in data:
        if row[4] == f'lc{star_id}.data':
            x_physical, y_physical = float(row[0]), float(row[1])
            #print(f"Coordenadas: X={x_physical}, Y={y_physical} para {row[4]}")
            break
    #else:
        #print(f"Estrella {star_id} no encontrada")
        
    return x_physical, y_physical
    
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils.aperture import CircularAperture, aperture_photometry

def get_m_ref(reference_fit, x_physical, y_physical, aperture_radius=7.0, display=False):
    """
    Calcula la magnitud instrumental en la imagen de referencia.
    
    Args:
        reference_fit: Path al archivo FITS de referencia
        x_physical, y_physical: Coordenadas físicas de la estrella
        aperture_radius: Radio de apertura en píxeles (debe coincidir con ISIS “rad_aper”)
    
    Returns:
        m_ref: Magnitud instrumental en la referencia
    """
    # 1. Cargar imagen de referencia
    with fits.open(reference_fit) as hdul:
        data = hdul[0].data
        header = hdul[0].header

    # 2. Convertir coordenadas físicas a píxeles
    x_pix = int(round(x_physical)) - 1
    y_pix = int(round(y_physical)) - 1

    # 3. Definir apertura
    position = (x_pix, y_pix)
    aperture = CircularAperture(position, r=aperture_radius)

    # 4. Calcular fotometría (C0 = 25 para DAOPHOT)
    phot_table = aperture_photometry(data, aperture)
    flux_ref = phot_table['aperture_sum'][0]
    C0 = 25.0
    m_ref = -2.5 * np.log10(flux_ref) + C0
    
    #m_ref = C0 - 2.5 * np.log10(flux_ref) + 2.5 * np.log10(exptime)

    # 5 (OPCIONAL). Mostrar imagen con apertura
    if display: 
        plt.figure(figsize=(6,6))
        plt.imshow(
            data,
            cmap='gray',
            origin='lower',
            vmin=np.percentile(data, 5),
            vmax=np.percentile(data, 99)
        )
        aperture.plot(color='red', lw=0.4)
        plt.colorbar(label='ADU (counts)')
        plt.title(f"Aperture photometry\nFlux={flux_ref:.2e}, m_ref={m_ref:.2f}")
        #plt.scatter(x_pix, y_pix, s=15, edgecolor='yellow', facecolor='none')
        plt.show()
        
        print('magnitud instrumental de la estrella en ref.fits:\n',m_ref,
      '\nflujo de la estrella en ref.fits\n' ,flux_ref)
        #return data, header, flux_ref, m_ref
    
    return m_ref, flux_ref

def get_m_ref_new(reference_fit, x_physical, y_physical, aperture_radius=7.0, exptime=1, display=False):
    if exptime == 1: print('🚨 No ingresaste exptime !')
    # 1. Cargar imagen de referencia
    with fits.open(reference_fit) as hdul:
        data = hdul[0].data
        header = hdul[0].header

    # 2. Convertir coordenadas físicas a píxeles
    x_pix = int(round(x_physical)) - 1
    y_pix = int(round(y_physical)) - 1

    # 3. Definir apertura
    position = (x_pix, y_pix)
    aperture = CircularAperture(position, r=aperture_radius)

    # 4. Calcular fotometría (C0 = 25 para DAOPHOT)
    phot_table = aperture_photometry(data, aperture)
    flux_ref = phot_table['aperture_sum'][0]
    C0 = 25.0
    m_ref = C0 - 2.5 * np.log10(flux_ref) + 2.5 * np.log10(exptime)

    # 5 (OPCIONAL). Mostrar imagen con apertura
    if display: 
        plt.figure(figsize=(6,6))
        plt.imshow(
            data,
            cmap='gray',
            origin='lower',
            vmin=np.percentile(data, 5),
            vmax=np.percentile(data, 99)
        )
        aperture.plot(color='red', lw=0.4)
        plt.colorbar(label='ADU (counts)')
        plt.title(f"Aperture photometry\nFlux={flux_ref:.2e}, m_ref={m_ref:.2f}")
        #plt.scatter(x_pix, y_pix, s=15, edgecolor='yellow', facecolor='none')
        plt.show()
        
        print('magnitud instrumental de la estrella en ref.fits:\n',m_ref,
      '\nflujo de la estrella en ref.fits\n' ,flux_ref)
        #return data, header, flux_ref, m_ref
    
    return m_ref, flux_ref


def isis_flux_to_mag(delta_flux, m_ref, C0=25):
    """
    Convierte flujos diferenciales de ISIS a magnitudes instrumentales.
    
    Args:
        delta_flux: Array de flujos diferenciales (ΔF_{*,i})
        m_ref: Magnitud instrumental en imagen de referencia (m_{*,ref})
        C0: Constante de calibración (default 25 para DAOPHOT)
    
    Returns:
        Array de magnitudes instrumentales
    """
    # Paso 1: Calcular F_{*,ref} usando m_ref
    F_ref = 10**((C0 - m_ref) / 2.5)
    
    # max: offset para evitar negativos 
    #offset = abs(delta_flux.min()) + 10
    offset =0
    # Paso 2: Calcular flujos absolutos: F_{*,i} = F_ref - ΔF_{*,i}
    absolute_flux = F_ref - delta_flux + offset
    
    # Paso 3: Convertir a magnitudes instrumentales
    mag_instr = -2.5 * np.log10(absolute_flux) + C0
    #C0 - 2.5 * np.log10(absolute_flux) + 2.5 * np.log10(exptime)
    
    return mag_instr


def isis_flux_to_mag_new(delta_flux, m_ref, exptime_list, C0=25):
    """
    Convierte flujos diferenciales de ISIS a magnitudes instrumentales.
    
    Args:
        delta_flux: Array de flujos diferenciales (ΔF_{*,i})
        m_ref: Magnitud instrumental en imagen de referencia (m_{*,ref})
        C0: Constante de calibración (default 25 para DAOPHOT)
    
    Returns:
        Array de magnitudes instrumentales
    """
    # Paso 1: Calcular F_{*,ref} usando m_ref
    F_ref = 10**((C0 - m_ref) / 2.5)
    
    # max: offset para evitar negativos 
    # 🐛 16_sept25: cambiamos el offset ya que nos traía Missing Values el anterior, no era suficiente offset: 
    #  abs(delta_flux.min()) + 10 -> abs((F_ref - delta_flux).min()) + 10
    offset = abs((F_ref - delta_flux).min()) + 10
    #offset =0
    # Paso 2: Calcular flujos absolutos: F_{*,i} = F_ref - ΔF_{*,i}
    absolute_flux = F_ref - delta_flux + offset
    
    # Paso 3: Convertir a magnitudes instrumentales
    #mag_instr = -2.5 * np.log10(absolute_flux) + C0
    mag_instr = C0 - 2.5 * np.log10(absolute_flux) + 2.5 * np.log10(exptime_list)
    
    return mag_instr