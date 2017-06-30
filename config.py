import yaml
from schema import Schema, And, Use, Regex, Optional
from plumbum import cli

config_schema = Schema ({
    'ifaces': {
        str: {
            'ssid': str,
            'pass': str
        }
    },
    'test': {
        'ifaces': [str],  # Each of these must be a key of the ifaces map.
        'wifi_iface': str, # The physical wifi network interface. (e.g., wlan0, wl3)
        Optional('pings', default=20): And(Use(int), lambda n: n > 0),
        Optional('ping_ip', default='8.8.8.8'): Regex(r'^\d+\.\d+\.\d+\.\d+$')
    },
    object: object
})

def read(filename):
    """Read, validate, and return the config file."""
    with open(filename) as f:
        config = yaml.safe_load(f)
    if config == None:
        raise Exception("No config at {}".format(filename))

    config = config_schema.validate(config)

    # Extra check: Every value test.ifaces[*] is a key of ifaces.
    iface_list = config['ifaces'].keys()
    for iface in config['test']['ifaces']:
        if iface not in iface_list:
            raise Exception("No iface configuration named {}".format(iface))

    return config

class ConfigCLI(cli.Application):
    "Validate config, and list available ifaces"
    def main(self, config_file):
        conf = read(config_file)

        names = [(iface, val['ssid']) for iface, val in conf['ifaces'].iteritems()]
        names.sort()

        maxlen = 0
        for (iface, _) in names:
            maxlen = max(len(iface), maxlen)
        for (iface, ssid) in names:
            print "{:{w}}  {}".format(iface, ssid, w=maxlen)

if __name__ == "__main__":
    ConfigCLI.run()
