from jinja2 import Template
import os

# Leer la plantilla
with open('template.j2', 'r') as f:
    template_content = f.read()

template = Template(template_content)

# Variables para cada conjunto de datos
variables = {
    'register_dir': 'register202506B_I',
    'images_dir': 'images202506B_I',
    'file_pattern': '202*o',
    'reference_file': '202506050244o',
    'saturation': '64000.0',
    'object_name': 'NGC6426'
}

# Renderizar la plantilla
output = template.render(**variables)

# Guardar el resultado
output_filename = f"{variables['register_dir']}_notion.md"
with open(output_filename, 'w') as f:
    f.write(output)

print(f"Archivo generado: {output_filename}")