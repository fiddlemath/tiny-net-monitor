# tiny-net-monitor
A tiny network monitoring toolkit, to throw on tiny computers, and keep lots of performance notes.

For the time being, these are intended to run only when a very particular setup is available. Conditions so far:

- Joining wifi networks is possible on the commandline with `ifup <wifi device>=<iface config>`. Individual networks are expected to be set up in `/etc/network/interfaces`, as per [this doc][wificonf]; though there will probably be a script here to partially automate that configuration.
- 

[wificonf]: https://help.ubuntu.com/community/NetworkConfigurationCommandLine/Automatic

## Setup
This isn't packaged or anything.

`pip install` the following packages:

* speedtest-cli
* plumbum
* schema
* PyYAML

## Plan

Gah. This is silly. Lighter, lighter.

- [X] iface schema
- [X] Script: From list of wifi configurations (Yaml file?),
  - get psk from wpa_passphrase
  - keep psk 
  - write out dedicated file in /etc/network/interfaces.

- [ ] Script: Cycle through config'd wifi interfaces, test each one, append to logfile.
  - [ ] Add timeouts and error handling to network managment functions
