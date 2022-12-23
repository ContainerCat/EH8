import json
from scapy.layers.l2 import Ether, ARP, srp
from scapy.layers.inet import IP, sr1, UDP, ICMP


def run(*args):
    print("[*] In module scapy")
    hosts = discoverHost("192.168.1.0/24")
    result = {"results": []}

    for x in hosts:
        os = discoverOS(x)
        ports = discoverPorts(x)
        temp = {"ip": x, "os": os, "ports": ports}
        result["results"].append(temp)

    data = json.dumps(result)

    return data


def discoverHost(range):
    """
    return all active hosts in a network
    """
    ips = []
    answer, unanswer = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=range), timeout=10)

    for sent, received in answer:
        ips.append(received.psrc)

    return ips


def discoverPorts(ip):
    """
    return all open ports of the ip
    """
    known_ports = [
        20,
        21,
        22,
        23,
        25,
        53,
        80,
        443,
        110,
        119,
        123,
        161,
        995,
        143,
        993,
        194,
    ]

    ports = []
    for x in known_ports:
        res = sr1(IP(dst=ip) / UDP(sport=x, dport=x), timeout=2)
        if res == None:
            ports.append(x)

        else:
            if res.haslayer(ICMP):
                continue
            elif res.haslayer(UDP):
                ports.append(x)
            else:
                continue

    return ports


def discoverOS(ip):
    res = sr1(IP(dst=ip) / ICMP(id=100), timeout=10)

    if res:
        if IP in res:
            ttl = res.getlayer(IP).ttl
            if ttl <= 64:
                return "Linux"
            elif ttl > 64:
                return "Windows"
            else:
                return None
        else:
            return None
    else:
        return None
