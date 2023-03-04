# BMC

BMC is a simple package to interact with the Turing Pi 2 BMC enabling features such as
turning on power to nodes.

## Usage

```python
from ipaddress import IPv4Address
from bmc.cluster import Cluster

cluster = Cluster(cluster_ip=IPv4Address('192.168.1.170'))
sdcard = cluster.get_sdcard()
print(sdcard)
```
