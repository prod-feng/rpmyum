# rpmyum
Python script to list rpm package information, Fedora10, yum-3.2.27. 

Developed on Fedora 10. May not be able to work on other system. July 2010.

This script to query detailed information of package. It uses part of codes of the PackageKit/PackageKit-yum packages.  Now it only support two query mode:


 1. Quey detailed information of a package
 ./rpmyum -d mypackage

 2. Query the what-requires of a package recursively
 ./rpmyum -r mypackage


 The following list the outs of the script as an example.

 This script runs pretty fast comparing the PackageKit and it's related GUI
 programs. It would also be interesting if to extend it to be more powerful
 as a good interactive system command.

=============================================
 
 
 query detailed dependencies of a package
 
=============================================

 [abc@localhost ~]$ ./rpmyum.py -r wireless-tools

     Retrieving the requires of package: wireless-tools :recursively

    #    Name    Summary

    1    system-config-keyboard;1.2.15-4.fc10;noarch;installed   A  graphical interface for modifying the keyboard

    2    booty;0.107-1.fc10;noarch;installed     simple python bootloader  config lib

    3    livecd-tools;020-1.fc10;i386;installed  Tools for building live  CD's

    4    firstboot;1.102-1.fc10;i386;installed   Initial system configuration utility

    5    system-config-network;1.5.93-2.fc10;noarch;installed    The GUI of the Network Adminstration Tool

    6    rhpxl;1.9-3.fc10;i386;installed Python library for configuring and  running X

    7    revisor-comps;2.1.2-2.fc10;noarch;installed     Revisor Comps  Files

    8    revisor-cli;2.1.2-2.fc10;noarch;installed       Revisor CLI  components

    9    revisor-comps;2.1.4-1.fc10;noarch;installed     Revisor Comps Files

    10    system-config-network-tui;1.5.93-2.fc10;noarch;installed The Network Adminstration Tool

    11    revisor-cli;2.1.4-1.fc10;noarch;installed       Revisor CLI  components

    12    revisor-gui;2.1.2-2.fc10;noarch;installed       Revisor GUI 
 
    13    system-config-firewall-tui;1.2.13-2.fc10;noarch;installed       A  text interface for basic firewall setup

    14    anaconda;11.4.1.62-1;i386;installed     Graphical system installer

    15    system-config-kickstart;2.7.20-1.fc10;noarch;installed  A graphical interface for making kickstart files

    16    system-config-display;1.1.1-1.fc10;noarch;installed     A graphical interface for configuring the X Window System display

    17    rhpl;0.218-1;i386;installed     Library of Python code used by installation and configuration tools

    18    system-config-firewall;1.2.13-2.fc10;noarch;installed   A graphical interface for basic firewall setup

    19    revisor;2.1.2-2.fc10;noarch;installed   Fedora "Spin" Graphical  User Interface

    20    system-config-users;1.2.81-1.fc10;noarch;installed      A  graphical interface for administering users and groups

    21    system-config-date;1.9.34-1.fc10;noarch;installed       A  graphical interface for modifying system date and time

    22    system-config-language;1.3.2-3.fc10;noarch;installed    A  graphical interface for modifying the system language

    Done!


 ==============================================
 
 
query detailed information of a package

================================================


 [abc@localhost ~]$ ./rpmyum.py -d wireless-tools

     Retrieving the detailed information of package: wireless-tools

     Package ID  :  wireless-tools;1:29-2.fc9;i386;installed

     Group       :  other

     Description :  This package contain the Wireless tools, used to manipulate  the Wireless Extensions. The Wireless Extension is an interface allowing  you to set Wireless LAN specific parameters and get the specific stats for  wireless networking equipment.

     Size        :  191  KB

     Files       :

    1  : /lib/libiw.so.29

    2  : /sbin/ifrename

    3  : /sbin/iwconfig

    4  : /sbin/iwevent

    5  : /sbin/iwgetid

    6  : /sbin/iwlist

    7  : /sbin/iwpriv

    8  : /sbin/iwspy

    9  : /usr/share/doc/wireless-tools-29/DISTRIBUTIONS.txt

    10  : /usr/share/doc/wireless-tools-29/INSTALL

    11  : /usr/share/doc/wireless-tools-29/README

    12  : /usr/share/man/man5/iftab.5.gz

    13  : /usr/share/man/man7/wireless.7.gz

    14  : /usr/share/man/man8/ifrename.8.gz

    15  : /usr/share/man/man8/iwconfig.8.gz

    16  : /usr/share/man/man8/iwevent.8.gz

    17  : /usr/share/man/man8/iwgetid.8.gz

    18  : /usr/share/man/man8/iwlist.8.gz

    19  : /usr/share/man/man8/iwpriv.8.gz

    20  : /usr/share/man/man8/iwspy.8.gz
