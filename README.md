![howdy neighbor!](https://y.yarn.co/8c6d3296-edf7-4cce-aaa5-2eec2b860849_screenshot.jpg)

## Hello, neighbor!

The neighbor app performs CDP and LLDP discovery on Ethernet interfaces. Usage is pretty basic at this time.

### Installation

pip3 install -r requirements.txt

### Usage

python3 neighbor.py

### Example

```
root@lab-infra01:~/# ./neighbor2.py | jq .
{
  "lo": {},
  "eno1": {
    "protocol": "LLDP",
    "neighbor": "switch02.arcanebyte.com",
    "platform": "n/a",
    "switchport": "Gi0/19",
    "state": "UP"
  },
  "eno2": {},
  "eno3": {},
  "eno4": {},
  "eno49": {
    "protocol": "LLDP",
    "neighbor": "switch02.arcanebyte.com",
    "platform": "n/a",
    "switchport": "Gi0/23",
    "state": "UP"
  },
  "ens2f0": {
    "protocol": "CDP",
    "neighbor": "switch01.arcanebyte.com",
    "platform": "cisco WS-C2960L-24TS-LL",
    "switchport": "GigabitEthernet0/2",
    "state": "UP"
  },
  "ens2f1": {},
  "eno50": {
    "protocol": "LLDP",
    "neighbor": "switch02.arcanebyte.com",
    "platform": "n/a",
    "switchport": "Gi0/24",
    "state": "UP"
  }
}
```
