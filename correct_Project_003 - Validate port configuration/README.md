# Validate switch port configuration
Motivation: Create a script to validate the configuration of switch ports.

This project consists of the following files:

- **check_iface_config.py**: main script.  
- **device_configuration**: suggested device configurations.  
- **helper.py**: responsible for reading and writing text files.  
- **inventory.yaml**: device inventory.  
- **port_template.yaml**: contains the configuration template for devices. This file defines the rules for commands that must be set on each interface.  
- **requirements.txt**: list of dependencies.  
- **validate_name_convention.py**: Python module that validates the naming convention of interface descriptions.

The validation is strictly based on each port’s description. In other words, the description configured on each port is used to validate the configuration of the other commands on that port.

Execução:
- Utilizar o laboratório : https://autonetops.com/labs/stp-root-guard/ or local lab using containerlab
- Carregar as configuraçções das portas. Utilizar o arquivo device_configuration.
- Instalar as dependências Arquivo requirements.
- Criar o diretório output
- Executar o arquivo: python3 check_iface_config.py
- Será exibido o output no terminal e será criado um arquivo para cada execução - baseado na data e hora da execução. Esta saída deve apresentar se a configuração está ok ou a divergência da configuração (o que precisa ser adicionado ou removido).




**Execution:**
1. Use the lab: [https://autonetops.com/labs/stp-root-guard/](https://autonetops.com/labs/stp-root-guard/) or a local lab using Containerlab.  
2. Load the port configurations using the `device_configuration` file.  
3. Install the dependencies listed in `requirements.txt`.  
4. Create the `output` directory.  
5. Run the script:  
   ```bash
   python3 check_iface_config.py