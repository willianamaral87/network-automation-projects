# Configuration Conversion Script from Enterasys to Huawei


## Step 1:
Backup the configuration of the Enterasys device
Save the file as switch-enterasys.txt


## Step 2:
Access the password vault and copy the admin and PSK passwords.
Fill in the passwords in the variables of the main script.

## Step 3:
Execute the script: 
```bash
python3 convert_enterasys_to_huawei.py
```

## Notes
The sensitive information was removed or replaced.

IP addresses were replaced with new IPs for testing purposes.