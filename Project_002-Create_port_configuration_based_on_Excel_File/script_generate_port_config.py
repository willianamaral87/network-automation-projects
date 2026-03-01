########## gerar_rotas.py
# Import required libraries
# For Jinja2 template rendering
from jinja2 import Environment, FileSystemLoader

# For reading YAML files (device configs and connection details)
import yaml

# For interactive debugging (use ipdb.set_trace() when needed)
import ipdb

# For pretty printing in the terminal
from rich import print as rprint

# For SSH connections to network devices
from netmiko import ConnectHandler

# Nome do arquivo YAML que foi convertido de XLSX para YAML.
yaml_file_name = 'portmapping.yaml'

with open(yaml_file_name,'r') as yaml_file:
    data = yaml.safe_load(yaml_file)

env = Environment(
    loader=FileSystemLoader("."), # Directory of the templates
    lstrip_blocks=True, # Remove whitespace before the blocks
    trim_blocks=True # Remove newline after the blocks
)

template = env.get_template("portas_template.j2")

#ipdb.set_trace()

rendered_template = template.render(data['inventory'])

#print('rendedizado:'.upper())
print(rendered_template)

# Salvar o hostname 
hostname = data['inventory']['hostname']

# Criar o arquivo
with open(f"config-{hostname}.cfg", "w") as f:
    f.write(rendered_template)