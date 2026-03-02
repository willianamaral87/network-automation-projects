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


Este trabalho consiste os arquivos abaixo, sendo eles:
- check_iface_config.py: script principal
- device_configuration: sugestão de configuração
- helper.py: responsável pela leitura e escrita de arquivos de texto
- inventory.yaml : inventário
- port_template.yaml: possui o template de configuração dos equipamentos. Este arquivo dita a regra dos comandos que precisam estar configurados em cada interface.
- requirements: dependências
- validate_name_convention.py: módulo em python que realiza a validação do name convention das descrições das portas.

Esta versão para validar a configuração de porta de switch, basea-se estritamente na descrição de cada porta, ou seja, a descrição configurada em cada porta é utilizada para validar a configuração dos outros comandos da porta.

Execução:
- Utilizar o laboratório : https://autonetops.com/labs/stp-root-guard/
- Carregar as configuraçções das portas. Utilizar o arquivo device_configuration.
- Instalar as dependências Arquivo requirements.
- Criar o diretório output
- Executar o arquivo: python3 check_iface_config.py
- Será exibido o output no terminal e será criado um arquivo para cada execução - baseado na data e hora da execução. Esta saída deve apresentar se a configuração está ok ou a divergência da configuração (o que precisa ser adicionado ou removido).
