################## IMPORT SESSIONS ##################
# Importa a classe ConnectHandler da biblioteca Netmiko para conectar a dispositivos de rede via SSH
from netmiko import ConnectHandler

# Importa o módulo logging para registrar mensagens de log e depuração
import logging

# Importa exceções do Netmiko para tratar erros de conexão, autenticação e timeout
# NetmikoTimeoutException : ocorre quando a conexão expira por tempo limite.
# NetmikoAuthenticationException : ocorre quando usuário ou senha estão errados.
# ReadTimeout → ocorre quando o dispositivo não responde a tempo durante a leitura de dados.
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException, ReadTimeout

# Importa a função para abrir e salvar arquivos
from helpers import read_yaml, save_file

# Importa o módulo time para usar funções relacionadas a tempo
import time
# Importa a classe datetime do módulo datetime para trabalhar com datas e horas
from datetime import datetime

################## Global Loggings ##################

# Configura o módulo logging
logging.basicConfig(
    # Define o arquivo onde os logs serão salvos
    filename='netmiko_debug.txt',
    # Define o nível mínimo de mensagens que serão registradas (DEBUG registra todas)
    level=logging.DEBUG,
    # Define o formato das mensagens de log: data/hora - nível - mensagem
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Cria um logger nomeado específico
logger = logging.getLogger('netmiko')

#####################################################

# Load devices from YAML file
devices = read_yaml("inventory_netmiko.yaml")

# Acessar cada device
for device in devices:
    # O Python tenta executar aqui, se erro ocorrer, o except evita de quebrar a execução.
    try:
        # Utiliza o Context Manager para gerenciar o Netmiko e abrir a conexão SSH com o dispositivo
        with ConnectHandler(**device['netmiko_conn']) as conn:

            # Anexar o timestamp para o Session logging
            with open(device['netmiko_conn']['session_log'], "a") as f:
                f.write(f"\n ###### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ###### \n")

            # Acessar o modo privilegiado - especial em ambientes multivendors
            conn.enable()

            # Imprimir na tela o device o sistema operacional do equipamento.
            print(f"\nConectado em {device['netmiko_conn']['host']} - ({device['netmiko_conn']['device_type']})")

            # Prepara o novo hostname
            new_hostname = f"hostname {device['extra']['new_hostname'].upper()}"

            # Enviar o comando de configuração do novo hostname ao switch.
            conn.send_config_set(new_hostname)

            # Atualizar o prompt esperado após alterar o hostname
            conn.set_base_prompt()

            # Salvar a configuração
            conn.save_config()

            # Imprimir a alteração do novo hostname
            print(f"The new hostname of {device['netmiko_conn']['host']} is {new_hostname}")

    # Trata o erro de timeout caso a conexão SSH não consiga se estabelecer, exemplo: falha de DNS ou se o device não estiver alcancavel.
    except NetmikoTimeoutException as e:
        print("TimeOut Error, possible reasons:\n Check DNS resolution")
        print(f"error: {e}")
    # Trata erro de credencial
    except NetmikoAuthenticationException as e:
        print("Authentication to device failed. Check the username and password")
        print(f"error: {e}")
    # Trata o erro caso o device type exista mas não é o device type correto do equipamento. 
    except ReadTimeout as e:
        print(f"The device type {device['netmiko_conn']['device_type']} exist but it is not compatible with the device")
        print(f"error: {e}")
    # Caso o device type não exista.
    except ValueError as e:
        print(f"The device type {device['netmiko_conn']['device_type']} does not exist. Check the correct on: {e}")
    # Tratar as exceptions não listadas acima
    except Exception as e:
        print(f"The error is: {e}")