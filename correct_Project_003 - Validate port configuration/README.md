# Validar a configuração de porta de switch.
Motivação: Criar um script para realizar a validação de configuração de porta de switch.

Esta entrega consiste em refatorar a atividade anterior, onde a mesma não estava escalável.

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
