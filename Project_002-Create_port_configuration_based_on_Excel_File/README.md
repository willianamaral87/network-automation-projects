# Generate Cisco switch port configurations automatically based on an Excel file.

Challenge: Simplify and accelerate switch port configuration using automation.

Approach: I structured the solution using four files:

- Input: An Excel file containing details such as interface name, data VLAN, voice VLAN, trunk port status, etc.

- Process: Two Python scripts:

	1) Script_convert_xls_yaml.py – responsible for reading the Excel file and converting it into a YAML file (human-readable format). This step uses Pandas to parse Excel data and then builds Python dictionaries to generate YAML.

	2) Script_generate_configuration.py – responsible for reading the YAML file and converting it into Cisco port configuration. Here, I used Jinja2 templates to apply business and security requirements.

- Output: A plain text file containing the generated switch configuration.

Advantages:
- Reduces human error.
- Saves time when configuring multiple switches.
- Splits responsibilities: one script generates the YAML, another generates the configuration.

Limitations:
- Jinja2 templates must be tailored to each organization’s requirements.
- The script currently doesn’t validate the Excel input, so accuracy depends on the analyst filling it correctly.
