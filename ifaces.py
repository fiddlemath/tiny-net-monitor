"""ifaces.py

Write the list of wifi networks and passwords to /etc/network/interfaces

-n: Don't write the list, just validate the configuration.
"""
import yaml
import config
from schema import Schema
from plumbum import cli

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
    return \
"""iface {} inet dhcp
      wpa-ssid "{}"
      wpa-psk {}

""".format(iface, ssid, psk)

def write_ifaces(ifaces, outfile):
    with open(outfile, 'w') as f:
        for iface, val in ifaces.iteritems():
            ssid, passwd = val['ssid'], val['pass']
            psk = get_psk(ssid, passwd)
            f.write(iface_definition(iface, ssid, psk))

class IFacesCLI(cli.Application):
    testonly = cli.Flag(["-t", "--test"],
                 help="Do not write the interfaces file; just validate.")
    
    def main(self,
             infile="~/net-monitor/config.yaml",
             outfile="/etc/network/interfaces.d/wifi_networks"):

        ifaces = config.read(infile)['ifaces']
        if not self.testonly:
            write_ifaces(ifaces, outfile)

if __name__ == "__main__":
    IFacesCLI.run()
