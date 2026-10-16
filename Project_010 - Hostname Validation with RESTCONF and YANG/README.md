# Cisco IOS-XE Hostname Automation with RESTCONF & YANG

A Python tool that collects, validates and changes hostnames on Cisco IOS-XE switches using **RESTCONF**. It validates every new hostname against the **Cisco YANG models plus a company naming standard** before anything is sent to a device.

> If any hostname in the inventory breaks the naming rule, the change is aborted and **no device is touched**.

---

## Why this project

Renaming dozens of switches by hand is slow and error-prone. A single typo in a hostname can break monitoring, documentation and naming conventions. This project:

- Reads the target devices and new hostnames from an Excel inventory
- Validates every hostname **offline - The validation runs locally on the machine (your laptop, a jump server, or a CI pipeline), without interacting with the switch itself.** with `yanglint`, using the official Cisco IOS-XE YANG model and a custom **YANG deviation** that enforces the company naming pattern
- Applies the change through RESTCONF only if **all** hostnames are valid
- Reads the hostname back from each device to confirm the change

---

## Features

| Option | Description |
|---|---|
| **1. Collect** | Reads the current hostname from every switch (RESTCONF `GET`) and can export the result to Excel |
| **2. Validate** | Validates hostnames with `yanglint`, either the **new** ones from the inventory or the **current** ones collected in option 1 |
| **3. Change** | Validates all new hostnames first, then applies them (RESTCONF `PATCH`) and confirms each change with a `GET` |
| **4. Save config** | *(planned)* Saves the running configuration |
| **5. Exit** | Closes the tool |

---

## How it works

```
inventory.xlsx ──► yanglint validation ──► all valid? ──no──► abort, nothing changed
                   (Cisco YANG +                │
                    company deviation)          yes
                                                ▼
                                    RESTCONF PATCH (new hostname)
                                                ▼
                                    RESTCONF GET (confirm change)
```

### YANG validation

Each hostname is wrapped in a payload such as:

```json
{"Cisco-IOS-XE-native:native": {"hostname": "VAR-SW-DEPART-22"}}
```

and validated with:

```bash
yanglint -Q -t edit -p xe/17131/ \
  xe/17131/Cisco-IOS-XE-native.yang \
  xe/17131/company-hostname-deviation.yang \
  payload.json
```

- `Cisco-IOS-XE-native.yang`: the official Cisco IOS-XE 17.13.1 model
- `company-hostname-deviation.yang`: a custom deviation that restricts the `hostname` leaf to the company naming standard (see below)

This catches invalid names **before** they reach the network, using the same data model the device uses.

### Hostname naming standard

Every hostname must follow the format:

```
SITE-TYPE-NAME-NUMBER
```

| Field | Rule | Example |
|---|---|---|
| **SITE** | Exactly 3 uppercase letters, the site code | `VAR`, `CRZ` |
| **TYPE** | Device type: `SW` (Switch), `RT` (Router) or `FW` (Firewall) | `SW` |
| **NAME** | 2 to 12 uppercase letters, the location or department | `IT`, `DEPART` |
| **NUMBER** | Last octet of the management IP, from 1 to 254, no leading zeros | `22` for `192.168.1.22` |

The fields are separated by hyphens (`-`).

| Hostname | Result | Reason |
|---|---|---|
| `VAR-SW-DEPART-22` | ✅ Valid | Follows the standard |
| `CRZ-RT-IT-1` | ✅ Valid | Follows the standard |
| `VARS-SW-IT-25` | ❌ Invalid | Site code has 4 letters |
| `VAR-AP-IT-25` | ❌ Invalid | `AP` is not an allowed device type |
| `VAR-SW-I-25` | ❌ Invalid | Name has only 1 letter |
| `VAR-SW-it-25` | ❌ Invalid | Name must be uppercase |
| `VAR-SW-IT-07` | ❌ Invalid | Leading zero in the number |
| `VAR-SW-IT-255` | ❌ Invalid | Number above 254 |
| `VAR-SW-IT` | ❌ Invalid | Missing the number |

The rule is enforced by a `pattern` statement in `company-hostname-deviation.yang`, which replaces the Cisco model's default `hostname` type:

```yang
deviation "/ios:native/ios:hostname" {
  deviate replace {
    type string {
      pattern '[A-Z]{3}-(SW|RT|FW)-[A-Z]{2,12}-'
            + '([1-9][0-9]?|1[0-9]{2}|2[0-4][0-9]|25[0-4])' {
        error-message
          "Hostname must follow SITE-TYPE_OF_DEVICE-LOCATION-IP, "
          + "e.g. VAR-SW-LOCATION-22";
      }
    }
  }
}
```

The number part of the pattern, `([1-9][0-9]?|1[0-9]{2}|2[0-4][0-9]|25[0-4])`, accepts only valid host octets: `1–99`, `100–199`, `200–249` and `250–254`.

> YANG patterns are implicitly anchored, so the whole hostname must match. No `^` or `$` is needed.

---

## Tech stack

- **Python 3**
- **RESTCONF** (RFC 8040) over HTTPS
- **YANG** models: Cisco IOS-XE native plus a custom deviation
- **yanglint** (libyang) for offline validation
- **requests**, **openpyxl**, **PyYAML**

---

## Project structure

```
Project_010 - Hostname Validation with RESTCONF and YANG/
├── hostname_manager.py      # Main menu and workflow
├── restconf.py                 # restconf_get / restconf_patch helpers
├── helpers.py                  # read_excel / save_excel helpers
├── requirements.txt
└── xe/17131/
    ├── Cisco-IOS-XE-native.yang
    ├── company-hostname-deviation.yang
    └── ...                     # dependent Cisco YANG modules
```

---

## Requirements

- Python 3.10+
- `yanglint` installed on the system (`sudo apt install yanglint` on Ubuntu/WSL)
- Cisco IOS-XE devices with RESTCONF enabled:

```
ip http secure-server
restconf
```

---

## Installation

```bash
git clone https://github.com/willianamaral87/network-automation-projects.git
cd "network-automation-projects/Project_010 - Hostname Validation with RESTCONF and YANG"

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Minimal dependencies:

```
pyyaml
requests
openpyxl
```

---

## Configuration

Credentials are provided through user input.


### Inventory file (`inventory.xlsx`)

| IP | new_hostname |
|---|---|
| 192.168.1.13 | CRZ-SW-IT-25 |
| 192.168.1.14 | VAR-SW-DEPART-22 |

- Row 1 is the header
- Column A is the device IP or FQDN
- Column B is the new hostname (only needed for option 3)

---

## Usage

```bash
python3 hostname_manager.py
```

```
===== HOSTNAME MENU =====
1. Collect the hostname on each switch
2. Validate hostname from Excel file
3. Change hostname
4. Save configuration
5. Exit

Select an option (1-5): 3
Function changing the hostname
OK       192.168.1.14  VAR-SW-DEPART-22
Sending config to each device
IP: 192.168.1.14 - Hostname: VAR-SW-DEPART-22 [OK]
```

Example of a blocked change:

```
INVALID  192.168.1.13  sw_test_01  -> ...pattern does not match...
There is an error in the hostname...
Aborting the script. Nothing was changed on the device
```

---

## Testing

The tool was tested against:

- **[Cisco DevNet Catalyst 8000 Always-On Sandbox](https://devnetsandbox.cisco.com/DevNet/environments/RsIUuBQY3YjF)**: a free, always-available IOS-XE lab from Cisco DevNet with RESTCONF enabled, so no reservation is needed
- **A real Cisco Catalyst 9300 switch**

To try it yourself, add the sandbox's IP or FQDN to `inventory.xlsx` and enter the credentials shown on the sandbox page when the script prompts for them. 
At the moment, the credentials are hardcoded in the script, so you don't need to type them. It will be removed soon.

### Simulating multiple devices with a single switch

Because testing was done with one switch, the script simulates multiple devices:
it reads the inventory file and changes the switch's hostname on each iteration,
as if each row were a different device.

If you're running it against more than one device, comment out the 3 lines in
`hostname_manager.py` marked with the comment that starts with
*"Since I'm testing this script with a single device..."*.

---

## Roadmap

- [ ] Option 4: save the running configuration (`cisco-ia:save-config` RPC)
- [ ] Dry-run mode that shows the changes without applying them
- [ ] Parallel execution for large inventories
- [ ] Logging to a file for audit trails
- [ ] Unit tests for the validation logic

---

## Author

**Willian Amaral**
Network Automation | Cisco | Python | RESTCONF/YANG

[LinkedIn](https://www.linkedin.com/in/wdamaral/)