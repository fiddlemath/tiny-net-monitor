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

- [ ] Config reader / validate option
  - [ ] Schema check
  - [ ] Check against available networking ifaces.
- [ ] General Logging (with datetimes, experiment data, sensible formatting)
- [X] Parse commands where needed
  - [ ] Test against tiny-box implementation!

- [ ] (Not code) Test keeping this in sync with some location. Probably just configure rsync.

- [ ] (Separate script) Read wireless config, update custom /etc/network/interfaces.d/ file.
