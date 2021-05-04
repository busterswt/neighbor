![howdy neighbor!](https://y.yarn.co/8c6d3296-edf7-4cce-aaa5-2eec2b860849_screenshot.jpg)

## Hello, neighbor!

The neighbor app performs CDP and LLDP discovery on Ethernet interfaces. Usage is pretty basic at this time.

### Installation

```
git clone https://github.com/busterswt/neighbor
pip3 install -r requirements.txt
```

### Usage

As root, run the following:

`python3 neighbor.py`

### Example

```
neighbor.py -h

Hello, neighbor!

usage: neighbor.py [-h] [--csv] [--json]

Grab CDP/LLDP neighbor information

optional arguments:
  -h, --help  show this help message and exit
  --csv       Provides output in csv format
  --json      Provides output in json format
```

```
# ./neighbor.py --csv

Hello, neighbor!

Listening for CDP and LLDP on eno1...
LLDP packet arrived on eno1
Listening for CDP and LLDP on eno2...
Layer ['LLDPDUSystemName'] not found - CDP/LLDP timeout or unexpected packet on eno2.
Listening for CDP and LLDP on eno49...
LLDP packet arrived on eno49
Interface eno3 is DOWN. Skipping!
Listening for CDP and LLDP on eno50...
LLDP packet arrived on eno50
Interface eno4 is DOWN. Skipping!
Listening for CDP and LLDP on ens1f0...
CDP packet arrived on ens1f0
Interface ens1f1 is DOWN. Skipping!
### Output written to lab-compute02_neighbors.csv ###

# cat lab-compute02_neighbors.csv
hostname,interface,protocol,neighbor,platform,switchport,state
lab-compute02,eno1,LLDP,switch02.arcanebyte.com,n/a,Gi0/15,UP
lab-compute02,eno2,timeout,timeout,timeout,timeout,UP
lab-compute02,eno49,LLDP,switch02.arcanebyte.com,n/a,Gi0/13,UP
lab-compute02,eno50,LLDP,switch02.arcanebyte.com,n/a,Gi0/14,UP
lab-compute02,ens1f0,CDP,switch01.arcanebyte.com,cisco WS-C2960L-24TS-LL,GigabitEthernet0/2,UP
```


