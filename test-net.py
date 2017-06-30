"""test-net.py

Test the speed and latency over time of some configured networks.
"""

import config
from plumbum import cli, local
from os import path
import re

def use_network_interface(wifi_iface, network_iface):
    # Bring up the interface
    ifup_outputs = local['ifup'][wifi_iface +'='+ network_iface].run()

    # Catch failures
    if not ifup_outputs[0]:
        raise Exception("Failed to connect to {}".format(network_iface))

    # Where's the DHCP server?
    stderr = ifup_outputs[2].splitlines()
    for line in stderr:
        m = re.match(r'DHCPACK of (\d+\.\d+\.\d+\.\d+) from (\d+\.\d+\.\d+\.\d+)',
                     line):
        if m:
            router_ip = m.group(2)
            break
    else:
        raise Exception("Didn't read server IP address out of ifup output")

    local['ip']('route', 'replace', 'default', 'via', router_ip)
    
def run_tests(test_config, log_name):

    with open(log_name, 'a') as log:
        log.write(datetime.now().strftime("%Y-%m-%d %X\n"))
        
    local['speedtest_cli']('--simple') >> log_name
    local['ping']('-c', test_config['pings'], test_config['ping_ip']) >> log_name
    
    with open(log_name, 'a') as log:
        log.write("\n")

class TestNetCLI(cli.Application):
    config_file = cli.SwitchAttr(['-c', '--config'],
                            str,
                            default="~/net-monitor/config.yaml")
    
    def main(self, outdir="~/net-monitor/log"):
        '''Run network tests for each configured interface.
        Append results to files in outdir'''

        config = config.read(self.config_file)

        for iface in config['ifaces']:
            use_network_interface(config['test']['wifi_iface'], iface)
            run_tests(config['test'], path.join(outdir, iface+'.log'))

if __name__ == "__main__":
    TestNetCLI.run()
