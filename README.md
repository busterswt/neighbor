## Installation

pip3 install -r requirements.txt

## Usage

python3 neighbor.py

## Example

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
