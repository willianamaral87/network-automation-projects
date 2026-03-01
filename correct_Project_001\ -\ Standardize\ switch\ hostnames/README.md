# Padronizar a configuração de hostname em switches e roteadores de diferentes fabricantes (multivendor),

Motivação: O objetivo deste laboratório é padronizar a configuração de hostname em switches e roteadores de diferentes fabricantes (multivendor), utilizando a biblioteca Netmiko para automatizar conexões SSH e aplicar as alterações de forma consistente e segura.

A padronização de hostname sugerida neste laboratório segue a convenção:
<SITE>-<AREA>-<TIPO-DEVICE>IP, onde:
- SITE : localidade do equipamento;
- AREA: área interna dentro da localidade;
- TIPO-DEVICE: tipo do dispositivo, como switch ou roteador;
- IP: quarto octeto do endereço IP do dispositivo.

Passo a Passo:
Para executar o script de alteração de hostname, são necessários 3 arquivos:
1) script-change-hostname.py : Script em Python responsável por aplicar a alteração de hostname nos dispositivos.

2) inventory_netmiko.yaml:
- Arquivo de inventário que contém a lista de dispositivos e suas informações de conexão.
- Estrutura:
- id: # Identificação do dispositivo
  netmiko_conn:
  
    host: r1                  # Hostname ou endereço IP do dispositivo

    username: admin           # Usuário

    password: autonetops      # Senha

    device_type: cisco_ios    # Tipo/fabricante do dispositivo

    session_log: r1_session_log.txt # Arquivo de log das execuções

    session_log_file_mode: append   # Modo append para não sobrescrever logs anteriores
  extra:
    new_hostname: SPO-OFFICE-SW11  # Novo hostname a ser aplicado

Observação: o arquivo de log (session_log) registra apenas os comandos executados no dispositivo, não grava erros de login ou problemas de resolução de hostname.

3) helpers.py
- Contém funções auxiliares, como a função para abrir e ler o inventário inventory_netmiko.yaml.
- Não é necessário alterar este arquivo.


Passos para execução:
1) Copie os 3 arquivos (script-change-hostname.py, inventory_netmiko.yaml e helpers.py) para o mesmo diretório.
2) Edite o arquivo inventory_netmiko.yaml para incluir os dados dos dispositivos que serão configurados, de acordo com o laboratório ou o ambiente de produção.

Executar o script:
python3.12 script-change-hostname.py 

Possíveis saídas mapeadas:

1) Execução bem sucedida:
python3.12 script-change-hostname.py 

    Conectado em r1 - (cisco_ios)
    The new hostname of r1 is hostname SPO-OFFICE-SW11

    Conectado em r2 - (cisco_ios)
    The new hostname of r2 is hostname RJO-PRODUCAO-SW12

    Conectado em r3 - (cisco_ios)
    The new hostname of r3 is hostname CPS-RH-SW13

    Conectado em r4 - (arista_eos)
    The new hostname of r4 is hostname LON-TI-SW14


2) Falha de DNS ou se o dispositivo não estiver alcançável:
TimeOut Error, possible reasons:
 Check DNS resolution
error: DNS failure--the hostname you provided was not resolvable in DNS: r6:22	


3) Em caso de credencial incorreta:
Authentication to device failed. Check the username and password
error: Authentication to device failed.

Common causes of this problem are:
1. Invalid username and password
2. Incorrect SSH-key file
3. Connecting to the wrong device

Device settings: cisco_ios r1:22

Authentication failed.


4)Caso o Netmiko suporte o Device type utilizado mas não é o device type correto do equipamento:
Utilizando o device_type juniper - onde o correto seria cisco_ios

Saída da execução do script utilizando o device_type juniper:
The device type juniper exist but it is not compatible with the device
error: 

Pattern not detected: 'Screen width set to' in output.

Things you might try to fix this:
1. Adjust the regex pattern to better identify the terminating string. Note, in
many situations the pattern is automatically based on the network device's prompt.
2. Increase the read_timeout to a larger value.

You can also look at the Netmiko session_log or debug log for more information.

5) Caso o device type não exista, temos a saída abaixo juntamente com uma lista dos devices types suportados:
The device type CISCO does not exist. Check the correct on: Unsupported 'device_type' currently supported platforms are: 

Segue a lista dos devices Cisco suportados:
cisco_apic
cisco_asa
cisco_ftd
cisco_ios
cisco_nxos
cisco_s200
cisco_s300
cisco_tp
cisco_viptela
cisco_wlc
cisco_xe
cisco_xr



