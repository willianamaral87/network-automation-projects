# Import YAML
import yaml

def read_yaml(path):
    with open(path, 'r') as f:
        device_list = yaml.safe_load(f)
    return device_list

def save_file(path, data):
    with open(path,'w') as f:
        f.write(data)

# Append the new content on the last file
def save_file_append(path, data):
    with open(path,'a') as f:
        f.write(data)

def save_file_append_with_datetime(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.txt"
    path = f"output/{filename}"

    with open(path, "a") as f:
        f.write(data)