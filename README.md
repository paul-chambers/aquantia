﻿Linux* aQuantia AQtion Driver for the aQuantia Multi-Gigabit PCI Express Family of
Ethernet Adapters
=============================================================================

May 05, 2017

Contents
========

- Important Note
- In This Release
- Identifying Your Adapter
- Building and Installation
- Command Line Parameters
- Additional Configurations
- Support

IMPORTANT NOTE
==============

WARNING:  The AQtion driver compiles by default with the LRO (Large Receive
Offload) feature enabled.  This option offers the lowest CPU utilization for
receives, but is completely incompatible with *routing/ip forwarding* and
*bridging*.  If enabling ip forwarding or bridging is a requirement, it is
necessary to disable LRO using compile time options as noted in the LRO
section later in this document.  The result of not disabling LRO when combined
with ip forwarding or bridging can be low throughput or even a kernel panic.

In This Release
===============

This file describes the aQuantia AQtion Driver for the aQuantia Multi-Gigabit PCI Express Family of
Ethernet Adapters.  This driver supports the linux kernels >= 3.10, 
and includes support for x86_64 and ARM Linux system.

This release contains source tarball and src.rpm package.

Identifying Your Adapter
========================

The driver in this release is compatible with AQC-100, AQC-107, AQC-108 based ethernet adapters.


SFP+ Devices (for AQC-100 based adapters)
----------------------------------

This release tested with passive Direct Attach Cables (DAC) and SFP+/LC Optical Transceiver.

Building and Installation
=========================

To manually build this driver:
------------------------------------------------------------
1. Move the base driver tar file to the directory of your choice. For example,
   use /home/username/aquantia.

2. Untar/unzip archive:

     tar zxf Aquantia-AQtion-1.6.7.tar.gz

3. Change to the driver src directory:

     cd Aquantia-AQtion-1.6.7/

4. Compile the driver module:
	make

5. Load the module:
    sudo insmod atlantic.ko
6. Unload the driver
	sudo rmmod atlantic

7. Install the driver in the system
    make && make install

    /lib/modules/[KERNEL_VERSION]/aquantia/atlantic.ko

8. Uninstall the driver:
	make uninstall
	or
	Run the following commands:
	sudo rm -f /lib/modules/`uname -r`/aquantia/atlantic.ko
	depmod -a `uname -r’


Or alternatively you can use Aquantia-AQtion-1.6.7-1.src.rpm
------------------------------------------------------------
1. Move the Aquantia-AQtion-1.6.7-1.src.rpm file to the directory of your choice. For example,
   use /home/username/aquantia.

2. Execute the commands:
    rpmbuild --rebuild Aquantia-AQtion-1.6.7-1.src.rpm
    sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/Aquantia-AQtion-1.6.7-1.x86_64.rpm
	
    After this driver will be installed.
    (You can check this via "rpm -qa | grep Aquantia")
	 

3. Uninstall the driver:
   Run the following commands:
   sudo rpm -e Aquantia-AQtion-1.6.7-1.x86_64

Check that the driver is working
------------------------------------------------------------
	
1. Verify ethernet interface appears:
	ifconfig
	or
	ip addr show
	
	If not new interface appears, check dmesg output.
	If you see "Bad firmware detected" please update firmware on your ethernet card.

2. Assign an IP address to the interface by entering the following, where
   x is the interface number:

    ifconfig ethX <IP_address> netmask <netmask>
    or
	ip addr add <IP_address> dev <DEV>
3. Verify that the interface works. Enter the following, where <IP_address>
   is the IP address for another machine on the same subnet as the interface
   that is being tested:

     ping  <IP_address>
      or (for IPv6)
     ping6 <IPv6_address>

Command Line Parameters
=======================
    Command line parameters are not supported in this release.


Config file parametes
=======================
Some parameters can be changed in the {source_dir}/aq_cfg.h file:

AQ_CFG_VECS_DEF
------------------------------------------------------------
Number of queues
Valid Range: 0 - 8 (up to AQ_CFG_VECS_MAX)
Default value: 4

AQ_CFG_IS_RSS_DEF
------------------------------------------------------------
Enable/disable Receive Side Scaling

This feature allows the adapter to distribute receive processing
across multiple CPU-cores and to prevent from overloading a single CPU core.

Valid values
0 - disabled
1 - enabled

Default value: 1

AQ_CFG_NUM_RSS_QUEUES_DEF
------------------------------------------------------------
Number of queues for Receive Side Scaling
Valid Range: 0 - 4 (up to AQ_CFG_VECS_DEF)

Default value: 4

AQ_CFG_IS_LRO_DEF
------------------------------------------------------------
Enable/disable Large Receive Offload

This offload enables the adapter to coalesce multiple TCP segments and indicate
them as a single coalesced unit to the OS networking subsystem.
The system consumes less energy but it also introduces more latency in packets processing.

Valid values
0 - disabled
1 - enabled

Default value: 1

After the aq_cfg.h file changed the driver must be rebuilt to take effect.

Additional Configurations
=========================
  Viewing Link Messages
  ---------------------
  Link messages will not be displayed to the console if the distribution is
  restricting system messages. In order to see network driver link messages on
  your console, set dmesg to eight by entering the following:

       dmesg -n 8

  NOTE: This setting is not saved across reboots.

  Jumbo Frames
  ------------
  The driver supports Jumbo Frames for all adapters. Jumbo Frames support is
  enabled by changing the MTU to a value larger than the default of 1500.
  The maximum value for the MTU is 16000.  Use the ifconfig command to
  increase the MTU size.  For example:

        ifconfig <ethX> mtu 9000 up

  ethtool
  -------
  The driver utilizes the ethtool interface for driver configuration and
  diagnostics, as well as displaying statistical information. The latest 
  ethtool version is required for this functionality.
 
  
  NAPI
  ----
  NAPI (Rx polling mode) is supported in the ixgbe driver. 

  See ftp://robur.slu.se/pub/Linux/net-development/NAPI/usenix-paper.tgz for 
  more information on NAPI.

Supported ethtool options
============================
 Viewing adapter settings
 ---------------------
 ethtool <ethX>
 
 Output example:
 Settings for enp1s0:
        Supported ports: [ ]
        Supported link modes:   100baseT/Full
                                1000baseT/Full
                                10000baseT/Full
        Supported pause frame use: Symmetric
        Supports auto-negotiation: Yes
        Advertised link modes:  100baseT/Full
                                1000baseT/Full
                                10000baseT/Full
        Advertised pause frame use: Symmetric
        Advertised auto-negotiation: Yes
        Speed: 10000Mb/s
        Duplex: Full
        Port: FIBRE
        PHYAD: 0
        Transceiver: external
        Auto-negotiation: on
        Link detected: yes

 ---
 Note: AQrate speeds (2.5/5 Gb/s) will be displayed only with linux kernels > 4.10.
    But you can still use these speeds:
	ethtool -s eth0 autoneg off speed 2500
		
 Viewing adapter  information
 ---------------------
 ethtool -i <ethX>

 Output example:
 driver: atlantic
 version: 1.6.7.0
 firmware-version: 1.5.49
 expansion-rom-version:
 bus-info: 0000:01:00.0
 supports-statistics: yes
 supports-test: no
 supports-eeprom-access: no
 supports-register-dump: yes
 supports-priv-flags: no

 Viewing Ethernet adapter statistics:
 ---------------------
 ethtool -S <ethX>

 Output example:
 NIC statistics:
     InPackets: 13238607
     InUCast: 13293852
     InMCast: 52
     InBCast: 3
     InErrors: 0
     OutPackets: 23703019
     OutUCast: 23704941
     OutMCast: 67
     OutBCast: 11
     InUCastOctects: 213182760
     OutUCastOctects: 22698443
     InMCastOctects: 6600
     OutMCastOctects: 8776
     InBCastOctects: 192
     OutBCastOctects: 704
     InOctects: 2131839552
     OutOctects: 226938073
     InPacketsDma: 95532300
     OutPacketsDma: 59503397
     InOctetsDma: 1137102462
     OutOctetsDma: 2394339518
     InDroppedDma: 0
     Queue[0] InPackets: 23567131
     Queue[0] OutPackets: 20070028
     Queue[0] InJumboPackets: 0
     Queue[0] InLroPackets: 0
     Queue[0] InErrors: 0
     Queue[1] InPackets: 45428967
     Queue[1] OutPackets: 11306178
     Queue[1] InJumboPackets: 0
     Queue[1] InLroPackets: 0
     Queue[1] InErrors: 0
     Queue[2] InPackets: 3187011
     Queue[2] OutPackets: 13080381
     Queue[2] InJumboPackets: 0
     Queue[2] InLroPackets: 0
     Queue[2] InErrors: 0
     Queue[3] InPackets: 23349136
     Queue[3] OutPackets: 15046810
     Queue[3] InJumboPackets: 0
     Queue[3] InLroPackets: 0
     Queue[3] InErrors: 0

 Disable GRO when routing/bridging
 ---------------------------------
 Due to a known kernel issue, GRO must be turned off when routing/bridging. 
 Its can be done with command:
 
 ethtool -K <ethX> gro off

 
 Disable LRO when routing/bridging
 ---------------------------------
 Due to a known kernel issue, LRO must be turned off when routing/bridging. 
 Its can be done with command:
 
 ethtool -K <ethX> lro off
 

Support
=======

If an issue is identified with the released source code on the supported
kernel with a supported adapter, email the specific information related
to the issue to rdc-drv@aquantia.com

License
=======

aQuantia Corporation Network Driver
Copyright(c) 2014 - 2017 aQuantia Corporation.

This program is free software; you can redistribute it and/or modify it
under the terms and conditions of the GNU General Public License,
version 2, as published by the Free Software Foundation.
