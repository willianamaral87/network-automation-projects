import yaml

def read_yaml(path):
    with open(path, 'r') as f:
        device_list = yaml.safe_load(f)
    return device_list

def save_file(path, data):
    with open(path,'w') as f:
        f.write(data)