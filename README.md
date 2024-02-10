# BMC

WARNING, This package is likely to change dramatically as I learn more about the Turing Pi 2 BMC API.

BMC is a simple package to interact with the Turing Pi 2 BMC API enabling features such as
turning on power to nodes.

Due to a change in how the API works in the Turing Pi 2, this package is not compatible with BMC < 2.0.0.

## Usage

```python
from ipaddress import IPv4Address
from bmc.cluster import Cluster

cluster = Cluster(cluster_ip=IPv4Address('192.168.1.170'), verify=False)
sdcard = cluster.nodes
print(sdcard)
```

## TODO

https://docs.turingpi.com/docs/turing-pi2-bmc-api

- [ ] Fix set_usb_mode
- [ ] Add support usb_boot
- [ ] Add support clear_usb_boot
- [ ] Add support node_to_msd
- [ ] Add support uart
- [ ] Add support firmware
- [ ] Add support flash
