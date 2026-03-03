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

## Prepare the environment:
- Go to the path:
  ```bash 
  cd /home/willian/my_projects/labs/
  ```
- Use a layer 2 image.

### Destroy the old the lab
  ```bash
  containerlab destroy -t lab_l2.clab.yaml 
  ```

### Deploy the lab: 
  ```bash
containerlab deploy -t lab_l2.clab.yaml 
  ```

### Create a new environment
  ```bash
python3 -m venv  venv
  ```

### Activate the virtual environment
  ```bash
source venv/bin/activate
  ```

**Execution:**
1. Create the `output` directory inside the path:
  ```bash
  cd /home/willian/my_projects/Project_003 - Validate port configuration
  ``` 

2. Install the dependencies listed in `requirements.txt` using pip3:
  ```bash
pip install netmiko
pip install genie
pip install pyats
  ``` 

3. Load the port configurations from the `device_configuration` file into each device.
  
3. Run the script:  
   ```bash
   python3 check_iface_config.py

   
## Notes:


Correct SSH:
  ```bash
ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 -oHostKeyAlgorithms=+ssh-rsa admin@172.20.20.11