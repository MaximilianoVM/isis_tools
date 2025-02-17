from phot_transformations import filter_light_curves, group_light_curves

def main():
    threshold = float(input("Ingresa el umbral minimo de conteo de pixeles: "))
    print("introduce los limites (physical) de tu imagen")
    xinf = float(input("x_inf:"))
    xsup = float(input("x_sup:"))
    yinf = float(input("y_inf:"))
    ysup = float(input("y_sup:"))
    seeing = int(input("Ingresa el valor del seeing (entero en pixeles): "))
    
    filter_light_curves(threshold=threshold, x_inf=xinf, x_sup=xsup, y_inf=yinf, y_sup=ysup)
    print("Filtrado completado: new_phot.data generado.")
    
    group_light_curves(seeing=seeing)
    print("Agrupamiento completado: sort_phot.data generado.")

if __name__ == "__main__":
    main()