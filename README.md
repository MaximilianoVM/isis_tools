Scripts auxiliares para la interpretación y filtrado de resultados con ISIS (image subtraction package): https://www.iap.fr/useriap/alard/package.html

En el manejo del paquete ISIS, es muy posible que se genere una gran cantidad de falsos positivos. El proposito de estas herramientas es el filtrado y facil identificación de los resultados realmente importantes.


📌 La carpeta **isis_tools** (con todo este repo) debe ser colocada en el directorio **package** de ISIS: **package/isis_tools**


## ✨ phot_processing.py
Se ejecutan las funciones de **phot_transformations.py** en orden, pidiendo por terminal los parametros requeridos: 
* umbral minimo de la ultima columna en **phot.data** (mayores valores pueden ser un buen indicio de variabilidad real)
* limites (physical) de tu imagen, consultar en ds9: valor minimo y maximo de los ejex **x** y **y**
* valor del seeing (entero en pixeles). Define un cuadrado, el lado debe ser igual al diametro en pixeles de una estrella promedio. Consultar en ds9 también.

Los archivos de salida son un listado filtrado y otro filtrado y agrupado. <br>
El agrupado se hace ya que varias curvas de luz pueden corresponder a una misma estrella. <br>
Ambos se encuentran en la carpeta _./outputs_.

🟢 Se ejecuta de la siguiente manera, con la terminal en el directorio isis_tools: `python3 phot_processing.py`

## ✨ save_lightcurves.py
Se ejecutan las funciones de **czerny.py** en orden.
Itera sobre todas las curvas de luz filtradas en **./outputs/filtered_phot.data** procesando cada una con la función **czerny** y guardando cada gráfica en **./imagenes_curvas**. 

De esta forma se crea un catalogo visualizable en dicha carpeta, donde se podrán identificar facilmente a ojo las curvas de luz sobresalientes.

  🟢 Se ejecuta de la siguiente manera, con la terminal en el directorio isis_tools: `python3 save_lightcurves.py`


## 📦️ Módulos

### phot_transformations.py
contiene las funciones **filter_light_curves** y **group_light_curves**. 
* **filter_light_curves:** Hace un filtrado de las curvas de luz listadas en **phot.data**, en base a un threshold para el abs value (ultima columna en dicho archivo) y a las dimensiones reales de las imagenes (consultar en **DS9**).
  La salida de la funcion es el archivo **outputs/filtered_phot.data**, que es el listado de curvas de luz filtradas.
* **group_light_curves:** Agrupa las curvas de luz de acuerdo a su proximidad, definiendo un cuadrado de lado solicitado.
  Requiere **outputs/filtered_phot.data** y la salida de la función es el archivo **outputs/grouped_phot.data**, donde los grupos se encuentran separados por un salto de linea.

### czerny.py
Contiene las dos funciones: **czerny** y **czerny_plot**
* **czerny:** Recibe el nombre de la curva de luz a procesar ej. 'lc580.data' y aplica el _metodo de Schwarzenberg-czerny (DOI 10.1086/309985)_, que busca periodicidad en las curvas de luz.
  Al final imprime el periodo calculado y escribe el archivo *./lc.data* con la curva de luz en fase.
*  **czerny_plot:** Grafica la curva de luz en fase generada por la funcion **czerny**.


### lightcurve_plots.py 
contiene una variedad de funciones para hacer gráficos de las curvas de luz: **plot_phase**, **plot_lc**, **plot_lc_gropued**
* **plot_phase:** recibe el path de la curva de luz generada por **czerny** ej. *lc_path='./images3/lc.data'*
* **plot_lc:** recibe el path de la curva de luz especifica que se desea graficar. ej. *lc_path='./images3/lc0.data'*
* **plot_lc_gropued:** requiere la lista *inputs/lc_list_group.data*, donde se listaran las curvas de luz a graficar en conjunto.
  

## 💬 apendice
**direcciones**
* '.' : directorio actual
* '..' : un directorio arriba
