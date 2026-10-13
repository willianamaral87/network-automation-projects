import requests   # sends HTTP requests to the device
import urllib3    # hides the SSL warning (see below)

# ---------------- SSL warning ----------------------------------
# The devices use a self-made (self-signed) certificate.
# Python doesn't trust it and prints a warning on every request.
# This line hides that warning. OK in a lab, NOT in production.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Headers for READING data (GET):
#   Accept -> "answer me in JSON"
HEADERS = {"Accept": "application/yang-data+json"}


# Headers for SENDING data (PATCH/PUT):
#   Accept       -> "answer me in JSON"
#   Content-Type -> "the data I'm sending you is JSON"
SEND_HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}

# How many seconds to wait for the device before giving up
TIMEOUT = 10

# ---------------- Function: read data from the device -----------
def restconf_get(host, username, password, path):
    """Send a RESTCONF GET to any path and return the JSON as a dict, or None."""

    # Glue the IP and the path together to make the full URL.
    # Example result:
    # https://192.168.1.13/restconf/data/Cisco-IOS-XE-native:native/hostname
    url = f"https://{host}{path}"

    # "try" = attempt this code. If something breaks, Python jumps
    # to the matching "except" below instead of crashing the script.
    try:
        # Send a GET request ("give me this data") to the device
        response = requests.get(
            url,                          # where to send it
            headers=HEADERS,              # ask for JSON
            auth=(username, password),    # log in
            verify=False,                 # don't check the certificate (lab)
            timeout=TIMEOUT,              # give up after TIMEOUT seconds
        )

        # Check the status code the device sent back.
        # 200 = OK -> continue normally.
        # 401 (bad login), 404 (bad path), 500 (device error)...
        #   -> this line raises an error and jumps to "except HTTPError"
        response.raise_for_status()

        # The device answered with text like:
        #   {"Cisco-IOS-XE-native:hostname": "CSR-Local"}
        # .json() turns that text into a Python dictionary,
        # and "return" sends it back to whoever called the function.
        return response.json()

    # ---- What to do if something goes wrong ----

    # The device answered, but with an error code (401, 404, 500...)
    except requests.exceptions.HTTPError:
        print(f"  HTTP error {response.status_code}: {response.text}")

    # Could not reach the device at all
    # (wrong IP, device off, RESTCONF not enabled...)
    except requests.exceptions.ConnectionError:
        print(f"  Could not connect to {host}")

    # The device took longer than TIMEOUT seconds to answer
    except requests.exceptions.Timeout:
        print(f"  Timed out after {TIMEOUT}s")

    # The device answered, but the text was not valid JSON
    except ValueError:
        print("  Response was not valid JSON")

    # We only get here if an error happened above.
    # None means "nothing / no result", so the caller knows it failed.
    return None

# ---------------- Function: change data on the device -----------
# Same idea as restconf_get, but it SENDS data instead of reading.
#   payload -> a Python dictionary with the new value, e.g.
#              {"Cisco-IOS-XE-native:hostname": "R1-NEW"}
# Returns True if it worked, False if it failed.
def restconf_patch(host, username, password, path, payload):
    """Send a RESTCONF PATCH (merge change) to a path. Return True/False."""

    url = f"https://{host}{path}"

    try:
        response = requests.patch(
            url,
            headers=SEND_HEADERS,         # we're sending JSON
            auth=(username, password),
            json=payload,                 # requests converts the dict to JSON text
            verify=False,
            timeout=TIMEOUT,
        )

        # 200 or 204 = success. 400/401/404... = error -> jump to except
        response.raise_for_status()
        return True

    # Same errors as in restconf_get()
    except requests.exceptions.HTTPError:
        print(f"  HTTP error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"  Could not connect to {host}")
    except requests.exceptions.Timeout:
        print(f"  Timed out after {TIMEOUT}s")

    return False