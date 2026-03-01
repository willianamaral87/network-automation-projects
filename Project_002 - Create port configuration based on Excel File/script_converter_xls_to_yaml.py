# Utilizar Pandas para ler o arquivo XLSX e converter em dicionário 
import pandas as pd
import yaml

import ipdb

# Nome do arquivo do Excel em formato XLSX
excel_file = "portmapping.xlsx"

# Le hostname da célula B1
hostname_df = pd.read_excel(excel_file, nrows=1, header=None)
hostname = hostname_df.iloc[0, 1]

# Le a tabela de interfaces a partir da linha 3, usando a linha 3 como cabeçalho
#df_ports = pd.read_excel(excel_file, skiprows=2, header=0)
df_ports = pd.read_excel(excel_file, skiprows=2, header=0, dtype=str)

#print(df_ports)

# Replace NaN (missing values) in a DataFrame with None
df_ports = df_ports.where(pd.notnull(df_ports), None)

# Converte para lista de dicionários
ports = df_ports.to_dict(orient="records")

# Monta o YAML
inventory = {
    "inventory": {
        "hostname": hostname,
        "ports": ports
    }
}

#ipdb.set_trace()

# Salvar em YAML

# Utilizar o hostname definido no arquivo do Excel
#yaml_file = f"{hostname}.yaml"

# usar hostname fixo com o mesmo nome do Excel
yaml_file = "portmapping.yaml"

# Criar o arquivo YAML
with open(yaml_file, "w") as f:
    yaml.dump(inventory, f, sort_keys=False, allow_unicode=True)

print(f"Arquivo YAML gerado: {yaml_file}")
