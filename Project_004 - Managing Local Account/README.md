# Project Overview: Managing Local Accounts on Network Devices with Ansible

The goal of this project is to keep local user accounts consistent across network devices, ensuring compliance with the company’s policies.

Even when a switch is configured with AAA, it is still necessary to maintain local accounts for several reasons, such as:
- Accessing the device if the TACACS server is unavailable
- Emergency access
- Initial device access during provisioning or troubleshooting
- Ensuring access during network or authentication infrastructure outages

This project consists of three Ansible playbooks:
- Remove all local accounts except the admin user and a predefined list of allowed users
- Remove a specific local user
- Create a new account or update the password if the user already exists

Advantages of this project
- Keeps the local user database on each switch consistent, containing only the necessary accounts with updated and standardized passwords
- Saves time by automatically removing unnecessary users
- Saves time by updating passwords across all switches simultaneously
- Allows easy creation of new accounts when needed, reducing manual work for the Network Team — especially in medium and large environments
- The playbooks are idempotent, ensuring the desired state is maintained after every execution.

In the attached screenshot, there is an example of removing all local accounts except the admin user and the allowed users.

Approved (homologated) users in this project:
- admin
- monitoring_tool
- service_now

Reference:
- https://docs.ansible.com/projects/ansible/latest/collections/cisco/ios/ios_user_module.html#ansible-collections-cisco-ios-ios-user-module
- AutoNetOps Couse: https://autonetops.com/

<img width="771" height="127" alt="1 - before" src="https://github.com/user-attachments/assets/4eba7006-22db-40df-9014-d96c9d20b715" />

<img width="552" height="245" alt="2 - script" src="https://github.com/user-attachments/assets/4698ccaa-d82a-499c-81cd-6dcd49ac0a4b" />

<img width="1574" height="501" alt="3 - output_execuration" src="https://github.com/user-attachments/assets/46865ec2-536c-4c11-b0b9-c3bacca79866" />

<img width="774" height="87" alt="4 - result" src="https://github.com/user-attachments/assets/60e1cf6b-0925-4066-8547-d68b93552aee" />


