import os
import nmap
import socket
from ipwhois import IPWhois
from dns.resolver import Resolver
from whois import WHOIS
import requests
from bs4 import BeautifulSoup

def port_scan(target):
    nm = nmap.PortScanner()
    nm.scan(target, '1-1024')
    return nm.all_hosts()

def dns_resolver(target):
    try:
        resolver = Resolver()
        answer = resolver.query(target)
        return answer[0].to_text()
    except Exception as e:
        return str(e)

def whois_lookup(target):
    try:
        w = WHOIS(target)
        return w.text
    except Exception as e:
        return str(e)

def ip_lookup(target):
    try:
        i = IPWhois(target)
        return i.lookup()['nets'][0]
    except Exception as e:
        return str(e)

def http_header_scan(target):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f'http://{target}/'
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()
    except Exception as e:
        return str(e)

def write_report(target):
    with open(f'report_{target}.doc', 'w') as f:
        f.write(f'Report for {target}\n\n')
        f.write('Port Scan Results:\n')
        nm = nmap.PortScanner()
        nm.scan(target, '1-1024')
        hosts = nm.all_hosts()
        for host in hosts:
            f.write(f'{host}: {nm[host].all_protocols()}')
        f.write('\n\nDNS Resolver Results:\n')
        dns_res = dns_resolver(target)
        f.write(dns_res)
        f.write('\n\nWhois Lookup Results:\n')
        whois_lookup_res = whois_lookup(target)
        f.write(whois_lookup_res)
        f.write('\n\nIP Lookup Results:\n')
        ip_lookup_res = ip_lookup(target)
        f.write(ip_lookup_res)
        f.write('\n\nHTTP Header Scan Results:\n')
        http_header_scan_res = http_header_scan(target)
        f.write(http_header_scan_res)

def main():
    target = input('Enter the target IP address: ')
    write_report(target)

if __name__ == '__main__':
    main()