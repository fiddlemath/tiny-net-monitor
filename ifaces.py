"""ifaces.py

Write the list of wifi networks and passwords to /etc/network/interfaces

-n: Don't write the list, just validate the configuration.
"""
import yaml
from schema import Schema
from plumbum import cli

iface_schema = Schema ([{
        'iface': str,
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

def iface_definition(iface, ssid, psk):
    """Returns the corresponding iface definition as a string,
    formatted for inclusion in /etc/network/interfaces.d/"""
    return """
iface {} inet dhcp
      wpa-ssid "{}"
      psk {}

""".format(iface, ssid, psk)

# def write_ifaces(ifaces, outfile='/etc/network/interfaces.d/'):

#     for network in ifaces:
#         definition = iface_definition(network['iface'],
#                                       network['ssid'],
#                                       network['psk'])
        

class IFacesCLI(cli.Application):
    testonly = cli.Flag(["t", "test"],
                    help="Do not write the interfaces file; just validate.")
    def main(self, filename="~/config/tiny-net-monitor"):
        ifaces = read_ifaces(filename)
        if not self.testonly:
            write_ifaces(ifaces)

if __name__ == "__main__":
    IFacesCLI.run()
