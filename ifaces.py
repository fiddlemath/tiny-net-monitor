"""ifaces.py

Write the list of wifi networks and passwords to /etc/network/interfaces

-n: Don't write the list, just validate the configuration.
"""
import yaml
from schema import Schema
from plumbum import cli

iface_schema = Schema ({
    'ifaces': {
        str: {
            'ssid': str,
            'pass': str
        }
    },
    str: object
})

def read_ifaces(filename):
    """Read and validate the config file."""
    with open(filename) as f:
        config = yaml.safe_load(f)
    if config == None:
        raise Exception("No config at {}".format(filename))

    return iface_schema.validate(config)['ifaces']

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

def write_ifaces(ifaces, outfile):
    with open(outfile, 'w') as f:
        for key, val in ifaces:
            f.write(iface_definition(key, val['ssid'], val['psk']))
        
class IFacesCLI(cli.Application):
    testonly = cli.Flag(["t", "test"],
                 help="Do not write the interfaces file; just validate.")
    
    def main(self,
             infile="~/config/tiny-net-monitor",
             outfile="/etc/network/interfaces.d/wifi_networks"):

        ifaces = read_ifaces(infile)
        if not self.testonly:
            write_ifaces(ifaces, outfile)

if __name__ == "__main__":
    IFacesCLI.run()
