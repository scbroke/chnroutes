# nnchnroutes - Non Non China Routes

**This is a modified version of [dndx/nchnroutes](https://github.com/dndx/nchnroutes) to adapt the reversed needs.**

## The original `nchnroutes`
The original `nchnroutes` was designed to pull IP addresses (blocks) of which stated themselves as 'CN' from [this APNIC list](https://ftp.apnic.net/stats/apnic/delegated-apnic-latest). The APNIC list might not be conclusive because it was not based on BGP announcements. The other list, [17mon/china\_ip\_list](https://github.com/17mon/china_ip_list), literally, containing China IP addresses and updates seasonally, might provide more precise information since this list was **mainly** generated based on BGP announcements. `nchnroutes` then integrates the data and subtracts them from the [IANA IPv4 Address Space Registry](https://www.iana.org/assignments/ipv4-address-space/ipv4-address-space.xhtml), resulting in a list containing all non-China IP addresses (blocks). Eventually `nchnroutes` generates `routes4.conf` and `routes6.conf` in BIRD static route format, and thus these files can be used in some cases, for example, pushing routes via OSPF.

## `nnchnroutes`?
In some cases, you want the reverse - for example, you might want to route China IP addresses through a specific (and pricy) transit that somehow routes China IP addresses better than your regular favorite transit. This project is designed to adapt to the reversed needs. The fundamentals of `nnchnroutes` are identical to `nchnroutes`, but one does addition and the other one does subtraction.

## Usage
The program only had few modification from `nnchnroutes`, so the following was borrowed from the original.

```
$ python3 produce.py -h

usage: produce.py [-h] [--include [CIDR [CIDR ...]]] [--next INTERFACE OR IP]
                  [--ipv4-list [{apnic,ipip} [{apnic,ipip} ...]]]

Generate China routes for BIRD.

optional arguments:
  -h, --help            show this help message and exit
  --include [CIDR [CIDR ...]]
                        IPv4 ranges to include in CIDR format
  --next INTERFACE OR IP
                        next hop for China IP addresses.
                        might be your transit address, might be your tunnel address.
  --ipv4-list [{apnic,ipip} [{apnic,ipip} ...]]
                        IPv4 lists to use when fetching China-based IP addresses,
                        multiple lists can be used at the same time (default:
                        apnic ipip)
```

To specify China IPv4 address list to use, use the `--ipv4-list` as the following:

* `python3 produce.py --ipv4-list ipip` - only use [17mon/china\_ip\_list](https://github.com/17mon/china_ip_list).
* `python3 produce.py --ipv4-list apnic` - only use [the APNIC list](https://ftp.apnic.net/stats/apnic/delegated-apnic-latest)
* `python3 produce.py --ipv4-list apnic ipip` - use both **(default)**

It is also possible to use `crontab` to generate `routes4.conf` and `routes6.conf` in certain time frequency.
