#!/usr/bin/env python
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import Link, TCLink, Intf
from mininet.node import CPULimitedHost
from mininet.cli import CLI
from mininet.log import setLogLevel
import os

if "__main__" == __name__:
	os.system("mn -c")

	setLogLevel("info")
	net = Mininet(link=TCLink)

	# Add hosts    
	h1 = net.addHost("h1")
	h2 = net.addHost("h2")

	# Add routers
	r1 = net.addHost("r1")
	r2 = net.addHost("r2")
	r3 = net.addHost("r3")
	r4 = net.addHost("r4")

	# Bandwidth
	bw1 = { "bw" : 1 }
	bw2 = { "bw" : 0.5 }

	# Host - router link
	net.addLink(h1, r1, max_queue_size = 60, use_htb=True, intfName1='h1-eth0', intfName2='r1-eth0', cls=TCLink, **bw1)
	net.addLink(h1, r2, max_queue_size = 60, use_htb=True, intfName1='h1-eth1', intfName2='r2-eth1', cls=TCLink, **bw1)
	net.addLink(h2, r3, max_queue_size = 60, use_htb=True, intfName1='h2-eth0', intfName2='r3-eth0', cls=TCLink, **bw1)
	net.addLink(h2, r4, max_queue_size = 60, use_htb=True, intfName1='h2-eth1', intfName2='r4-eth1', cls=TCLink, **bw1)

	# Router - router link
	net.addLink(r1, r3, max_queue_size = 60, use_htb=True, intfName1='r1-eth1', intfName2='r3-eth1', cls=TCLink, **bw2)
	net.addLink(r1, r4, max_queue_size = 60, use_htb=True, intfName1='r1-eth2', intfName2='r4-eth2', cls=TCLink, **bw1)
	net.addLink(r3, r2, max_queue_size = 60, use_htb=True, intfName1='r3-eth2', intfName2='r2-eth2', cls=TCLink, **bw1)
	net.addLink(r2, r4, max_queue_size = 60, use_htb=True, intfName1='r2-eth0', intfName2='r4-eth0', cls=TCLink, **bw2)

	net.build()

	# IP config h1 & h2
	h1.cmd("ifconfig h1-eth0 0")
	h1.cmd("ifconfig h1-eth1 0")
	h1.cmd("ifconfig h1-eth0 192.168.0.1 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 192.168.5.2 netmask 255.255.255.0")

	h2.cmd("ifconfig h2-eth0 0")
	h2.cmd("ifconfig h2-eth1 0")
	h2.cmd("ifconfig h2-eth0 192.168.2.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 192.168.3.1 netmask 255.255.255.0")

	# IP config r1 - r4
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	r1.cmd("ifconfig r1-eth0 192.168.0.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.1.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.6.1 netmask 255.255.255.0")

	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	r2.cmd("ifconfig r2-eth0 192.168.4.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.5.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.7.1 netmask 255.255.255.0")

	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	r3.cmd("ifconfig r3-eth0 192.168.2.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.1.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.7.2 netmask 255.255.255.0")

	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	r4.cmd("ifconfig r4-eth0 192.168.4.1 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.3.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.6.2 netmask 255.255.255.0")

	# Config routers
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	# r1.cmd("sysctl net.ipv4.ip_forward=1")
	# r2.cmd("sysctl net.ipv4.ip_forward=1")
	# r3.cmd("sysctl net.ipv4.ip_forward=1")
	# r4.cmd("sysctl net.ipv4.ip_forward=1")
  	
	# STATIC ROUTING
	h1.cmd("ip rule add from 192.168.0.1 table 1")
	h1.cmd("ip rule add from 192.168.5.2 table 2")
	h1.cmd("ip route add 192.168.0.0/24 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 192.168.0.2 dev h1-eth0 table 1")
	h1.cmd("ip route add 192.168.5.0/24 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 192.168.5.1 dev h1-eth1 table 2")
	h1.cmd("ip route add default scope global nexthop via 192.168.0.2 dev h1-eth0")

	h2.cmd("ip rule add from 192.168.2.2 table 1")
	h2.cmd("ip rule add from 192.168.3.1 table 2")
	h2.cmd("ip route add 192.168.2.0/24 dev h2-eth0 scope link table 1")
	h2.cmd("ip route add default via 192.168.2.1 dev h2-eth0 table 1")
	h2.cmd("ip route add 192.168.3.0/24 dev h2-eth1 scope link table 2")
	h2.cmd("ip route add default via 192.168.3.2 dev h2-eth1 table 2")
	h2.cmd("ip route add default scope global nexthop via 192.168.2.1 dev h2-eth0")

	r1.cmd("route add -net 192.168.2.0/24 gw 192.168.1.2")
	r1.cmd("route add -net 192.168.3.0/24 gw 192.168.6.2")
	r1.cmd("route add -net 192.168.4.0/24 gw 192.168.6.2")
	r1.cmd("route add -net 192.168.5.0/24 gw 192.168.6.2")
	r1.cmd("route add -net 192.168.7.0/24 gw 192.168.1.2")

	r2.cmd("route add -net 192.168.0.0/24 gw 192.168.7.2")
	r2.cmd("route add -net 192.168.1.0/24 gw 192.168.7.2")
	r2.cmd("route add -net 192.168.2.0/24 gw 192.168.7.2")
	r2.cmd("route add -net 192.168.3.0/24 gw 192.168.4.1")
	r2.cmd("route add -net 192.168.6.0/24 gw 192.168.4.1")

	r3.cmd("route add -net 192.168.3.0/24 gw 192.168.7.1")
	r3.cmd("route add -net 192.168.4.0/24 gw 192.168.7.1")
	r3.cmd("route add -net 192.168.5.0/24 gw 192.168.7.1")
	r3.cmd("route add -net 192.168.0.0/24 gw 192.168.1.1")
	r3.cmd("route add -net 192.168.6.0/24 gw 192.168.1.1")

	r4.cmd("route add -net 192.168.2.0/24 gw 192.168.6.1")
	r4.cmd("route add -net 192.168.1.0/24 gw 192.168.6.1")
	r4.cmd("route add -net 192.168.0.0/24 gw 192.168.6.1")
	r4.cmd("route add -net 192.168.5.0/24 gw 192.168.4.2")
	r4.cmd("route add -net 192.168.7.0/24 gw 192.168.4.2")


	h2.cmdPrint("iperf -s &")
	h1.cmdPrint("iperf -t 10 -c 192.168.2.2 &")

	print("r1 ke h2")
	r1.cmdPrint("ping -c 3 192.168.2.2")

	print("h1 ke r3")
	h1.cmdPrint("ping -c 3 192.168.2.1")

	CLI(net)
	net.stop()
