import numpy as np

# filtra por dimensiones y threshold de abs_value (ultima columna)
def filter_light_curves(threshold=0, x_inf=0, x_sup=10, y_inf=0, y_sup=10):
    
    input_file='../register3/phot.data' # archivo a procesar (en register#)
    output_file='./outputs/filtered_phot.data' # archivo que vamos a generar (no estoy seguro donde)
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            data = line.strip().split()
            # salta lineas incompletas:
            if len(data) < 7:
                continue  
            # extraemos:
            abs_value = float(data[6])
            x, y = float(data[0]), float(data[1])
            # discriminamos:
            if x>x_inf and x<x_sup and y>y_inf and y<y_sup and abs_value > threshold:
                outfile.write(line)

# agrupa las lc por proximidad 
def group_light_curves(seeing=0):
    
    input_file='./outputs/filtered_phot.data'
    output_file='./outputs/grouped_phot.data'
    
    data = []
    # leemos los datos y guardamos en data=[]
    with open(input_file, 'r') as infile:
        for line in infile:
            parts = line.strip().split()
            if len(parts) < 7:
                continue
            x_r, y_r = float(parts[0]), float(parts[1])
            x_int, y_int = int(parts[2]), int(parts[3])
            name, var, abs_value = parts[4], float(parts[5]), float(parts[6])
            data.append([x_r, y_r, x_int, y_int, name, var, abs_value, 0])  # 0 indica si ya fue usado
    
    # escribimos el filtrado recorriendo el data=[] llenado anteriormente
    with open(output_file, 'w') as outfile:
        # enumerate se usa para recorrer la lista data 
        # y obtener tanto el índice como el valor de cada fila.
        for i, row_i in enumerate(data):
            if row_i[7] == 1:
                continue  # Ya fue agrupado
            xi, yi = row_i[2], row_i[3]
            
            for j, row_j in enumerate(data):
                if row_j[7] == 0:
                    xj, yj = row_j[2], row_j[3]
                    if abs(xi - xj) <= seeing and abs(yi - yj) <= seeing:
                        outfile.write(f"{row_j[0]:.6f} {row_j[1]:.6f} {row_j[2]} {row_j[3]} {row_j[4]} {row_j[5]:.4f} {row_j[6]:.4f}\n")
                        data[j][7] = 1 # lo marcamos como ya agrupado
            # separa grupos por espacio:
            outfile.write('\n') 