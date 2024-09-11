#!/usr/bin/env python3
import argparse
import csv
from ipaddress import IPv4Network, IPv6Network
import math

parser = argparse.ArgumentParser(description='Generate China routes for BIRD.')
parser.add_argument('--include', metavar='CIDR', type=str, nargs='*',
                    help='IPv4 ranges to include in CIDR format')
parser.add_argument('--next', default="wg0", metavar = "INTERFACE OR IP",
                    help='next hop for China IP address, this is usually the tunnel interface')
parser.add_argument('--ipv4-list', choices=['apnic', 'ipip'], default=['apnic', 'ipip'], nargs='*',
                    help='IPv4 lists to use when including China based IP, multiple lists can be used at the same time (default: apnic ipip)')

args = parser.parse_args()

class Node:
    def __init__(self, cidr, parent=None):
        self.cidr = cidr
        self.child = []
        self.dead = False
        self.parent = parent

    def __repr__(self):
        return "<Node %s>" % self.cidr

def dump_tree(lst, ident=0):
    for n in lst:
        print("+" * ident + str(n))
        dump_tree(n.child, ident + 1)

def dump_bird(lst, f):
    for n in lst:
        if n.dead:
            continue

        if len(n.child) > 0:
            dump_bird(n.child, f)

        elif not n.dead:
            f.write('route %s via "%s";\n' % (n.cidr, args.next))

INCLUDE = []
INCLUDE_V6 = []
if args.include:
    for e in args.include:
        if ":" in e:
            INCLUDE_V6.append(IPv6Network(e))

        else:
            INCLUDE.append(IPv4Network(e))

IPV6_UNICAST = IPv6Network('2000::/3')

def add_cidr(add_to, add_by):
    for cidr_to_add in add_by:
        add_to.append(Node(cidr_to_add))

root = []
root_v6 = [Node(IPV6_UNICAST)]

with open("delegated-apnic-latest") as f:
    for line in f:
        if 'apnic' in args.ipv4_list and "apnic|CN|ipv4|" in line:
            line = line.split("|")
            a = "%s/%d" % (line[3], 32 - math.log(int(line[4]), 2), )
            a = IPv4Network(a)
            add_cidr(root, (a,))

        elif "apnic|CN|ipv6|" in line:
            line = line.split("|")
            a = "%s/%s" % (line[3], line[4])
            a = IPv6Network(a)
            add_cidr(root_v6, (a,))

if 'ipip' in args.ipv4_list:
    with open("china_ip_list.txt") as f:
        for line in f:
            line = line.strip('\n')
            a = IPv4Network(line)
            add_cidr(root, (a,))

# add included addresses
add_cidr(root, INCLUDE)
add_cidr(root_v6, INCLUDE_V6)

with open("routes4.conf", "w") as f:
    dump_bird(root, f)

with open("routes6.conf", "w") as f:
    dump_bird(root_v6, f)
