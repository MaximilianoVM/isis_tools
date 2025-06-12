import os

DATA_DIR_1 = str(input("DATA_DIR: ej. 'NGC_6426I' \n"))
DATA_DIR_2 = str(input("DATA_DIR_2: ej. 'NGC_6426I_2' \n"))
DATA_MERGED_DIR = str(input("DATA_MERGED_DIR: ej. '6426I_MERGED' \n"))
CORR_FILE = f"{DATA_MERGED_DIR}/correspondences.csv"

os.makedirs(DATA_MERGED_DIR, exist_ok=True)

with open(CORR_FILE, "r") as f:
    lines = f.readlines()

# saltar encabezados (dos primeras líneas)
for line in lines[2:]:
    set1_file, set2_file = line.strip().split(",")

    # rutas
    path1 = os.path.join(DATA_DIR_1, set1_file)
    path2 = os.path.join(DATA_DIR_2, set2_file)

    # leer contenido de ambos archivos
    with open(path1, "r") as f1:
        data1 = f1.read()

    with open(path2, "r") as f2:
        data2 = f2.read()

    # extraer numeros para construir nombre del archivo combinado
    num1 = set1_file.replace("lc", "").replace(".data", "")
    num2 = set2_file.replace("lc", "").replace(".data", "")

    merged_filename = f"lc{num1}_{num2}.data"
    merged_path = os.path.join(DATA_MERGED_DIR, merged_filename)

    with open(merged_path, "w") as fout:
        fout.write(data1.strip() + "\n" + data2.strip() + "\n")

    print(f"✅ Archivo combinado: {merged_filename}")

