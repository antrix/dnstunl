#!/usr/bin/env python
"""
Generate a `dnsmasq` configuration file for use with services like
Tunlr, Unblock-Us and UnoDNS.

Usage: Configure the handful of constants below and execute the script.

Copyright (c) 2013 Deepak Sarda

This and other files in this directory are licensed under the MIT license.
See LICENSE file for details.
"""

# Where do we get the list of domains from, and where do we write to
SOURCE_FILE = 'domains.txt'
TARGET_FILE = 'dnsmasq.conf'

# Here we define the servers that serve a certain region,
# most have the same one(s) for all regions
# tunlr.net
# BYPASS_NAMESERVERS = dict(
#                         US=('69.197.169.9', '192.95.16.109'),
#                         UK=('69.197.169.9', '192.95.16.109'),
#                         CA=('69.197.169.9', '192.95.16.109')
#                         )
# unodns
BYPASS_NAMESERVERS = dict(
                        US=('122.248.238.233', '14.136.236.187'),
                        UK=('122.248.238.233', '14.136.236.187'),
                        CA=('122.248.238.233', '14.136.236.187')
                        )
# ibDNS has single servers per region, that's why we enter only one here
# BYPASS_NAMESERVERS = dict(
#                             US=('173.208.120.194',),
#                             UK=('31.3.254.2',),
#                             CA=('142.4.213.95',)
#                             )

# The DNS server to use when a domain is not in the list.
# Have a look at namebench : https://code.google.com/p/namebench/
# to see which default server is fast for you
# These are just here as sensible defaults
# OpenDNS
DEFAULT_NAMESERVERS = ('208.67.220.220', '208.67.222.222')
# Google Public DNS : https://developers.google.com/speed/public-dns/
# DEFAULT_NAMESERVERS = ('8.8.8.8', '8.8.4.4')

# Some domains you want to add always, regardless of what is in the input file
ADDITIONAL_DOMAINS = ('US,tunlr.net', 'US,unotelly.com')

# Header of the configuration file
# From http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html
# -D, --domain-needed
#   Tells dnsmasq to never forward A or AAAA queries for plain names,
#   without dots or domain parts, to upstream nameservers. If the name is
#   not known from /etc/hosts or DHCP then a "not found" answer is returned.
# --all-servers
#   By default, when dnsmasq has more than one upstream server available, it
#   will send queries to just one server. Setting this flag forces dnsmasq
#   to send all queries to all available servers. The reply from the server
#   which answers first will be returned to the original requester.
# -c, --cache-size=<cachesize>
#   Set the size of dnsmasq's cache. The default is 150 names. Setting the
#   cache size to zero disables caching.
# -o, --strict-order
#   By default, dnsmasq will send queries to any of the upstream servers it
#   knows about and tries to favour servers that are known to be up. Setting
#   this flag forces dnsmasq to try each query with each server strictly in
#   the order they appear in /etc/resolv.conf

PREFIX_CONFIG = """domain-needed
all-servers
cache-size=5000
strict-order
"""


# Function to write out the domains and nameservers
def write_server_lines(fp, servers, domains):
    for domain in domains:
        # Grab the region from the first item on the line
        region = domain.split(',')[0]
        # And the domain from the next
        domain = domain.split(',')[1]
        # Loop over the servers of a region, and add them to the domain
        for ns in servers[region]:
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
