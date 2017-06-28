"""ifaces.py

Write the list of wifi networks and passwords to /etc/network/interfaces

-n: Don't write the list, just validate the configuration.
"""
import yaml
from schema import Schema

iface_schema = Schema ([
    {
        'iface': str
        'ssid': str,
        'pass': str
    }])

def read_ifaces(filename):
    """Read and validate the config file."""
    with open(filename) as f:
        config = yaml.safe_load(f)
    if config == None:
        raise Exception("No config at {}".format(filename))

    return iface_schmea.validate(config)

from plumbum.cmd import wpa_passphrase
def get_psk(ssid, password):
    output = wpa_passphrase(ssid, password)
    
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("psk="):
            return line[4:]

    
