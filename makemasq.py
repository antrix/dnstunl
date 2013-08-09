#!/usr/bin/env python
"""
Generate a `dnsmasq` configuration file for use with services like Tunlr, Unblock-Us and UnoDNS.

Usage: Configure the handful of constants below and execute the script.

Copyright (c) 2013 Deepak Sarda

This and other files in this directory are licensed under the MIT license. 
See LICENSE file for details.
"""

SOURCE_FILE = 'domains.txt'
TARGET_FILE = 'dnsmasq.conf'

BYPASS_NAMESERVERS = ('69.197.169.9', '192.95.16.109')
# Viewqwest
# DEFAULT_NAMESERVERS = ('202.73.37.3', '202.73.37.11')
# OpenDNS
DEFAULT_NAMESERVERS = ('208.67.220.220', '208.67.222.222')
ADDITIONAL_DOMAINS = ('tunlr.net',)

PREFIX_CONFIG = """domain-needed
all-servers
cache-size=5000
"""

def write_server_lines(fp, servers, domains):
    for domain in domains:
        for ns in servers:
            fp.write('server=/%s/%s\n' % (domain, ns))
    fp.write('\n')

def main():
    target = open(TARGET_FILE, 'w')

    target.write(PREFIX_CONFIG)
    target.write('\n\n')

    all_domains = open(SOURCE_FILE).readlines()

    all_domains = (d.strip() for d in all_domains)

    write_server_lines(target, BYPASS_NAMESERVERS, all_domains)
    write_server_lines(target, BYPASS_NAMESERVERS, ADDITIONAL_DOMAINS)
    
    target.write('# Default DNS\n')

    for ns in DEFAULT_NAMESERVERS:
        target.write('server=%s\n' % (ns,))

    target.close()

if __name__ == '__main__':
    main()
