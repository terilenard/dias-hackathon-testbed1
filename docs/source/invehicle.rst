1. In Vehicle Setup
===================

This page describes how to setup the In Vehicle machine. The github project contains a dedicated directory named **toolchain** where a directory containing setup scripts exists.
Those scripts are meant to install dependencies, compile required libraries, and install modules. Those scripts run both, root and non-root commands. The scripts should be run
as normal user. If a script needs to run a command as root, it will ask at one point for the root password. As such, do not run the scripts as root. The scripts are meant to automate the install process and should be run in the order mentioned below. Some may take a longer time to run, since compilation of some libraries take time. 

The In-Vehicle setup is meant to simulate a Controller Area Network (CAN) system inside a linux based system. Inside the linux box a virtual CAN (vcan) is used to simulate the CAN bus. Each component connects to this CAN bus to listen or exchange messages.

This machine can be configured in two main ways:

1. As a Ubuntu Virtual Machine
2. As a RaspberryPi (TODO)

If the testbed is configured for option 1, then the *CAN2UDP* service must be installed, to allow user to connect to the virtual CAN bus from exterior, withtout having direct access to the software running in the linux box. If option 2 is chosen, then the *CAN2UDP* service is optional, but a additional *CANGW* service must be install so that the traffic from the virtual can is forwarded to the CAN bus connected to the RaspberryPi, and vice-versa.

1.1 Requirements
----------------

As mentioned, the In-Vehicle machine can be configured on one of the followings systems:

1. Raspberry Pi 4 (recommended) with Rasbian latest version. Consider at least 32?? gb SD card. The 2GB and 4GB boards, may require additional memory to compile some libraries. This is why we don't recomand Raspberry Pi 3s. Even tho, the system can be installed and configured if a large enaugh SWAP is configured on the board. To increase the SWAP size of your board follow Section 1.3 first.

2. Ubuntu 20.04 LTS virtual machine (recommended and tested). For Ubuntu virtual machine set a minimum 30gb storage and 5gb RAM memory. Be sure besides this, to set at least 2-4 cores to the virtual machine to speedup the compilation process for several libraries. As for networking, configure the virtual machine network interface to run Bridge mode.

1.2 Instalation
---------------

Before starting the actuall installation, be sure to update your machine, and download the respository.

.. code-block:: bash

   sudo apt -y update

.. code-block:: bash

    sudo apt install -y git python3-pip net-tools
   
A separate directory in which you can work is nice:

.. code-block:: bash
 
    mkdir Workspace ; cd Workspace
    
The repository must be clonned recursively since it contains inside other git repositories. And those repositories may contain inside other git repositories (e.g., kuksa.val).

.. code-block:: bash

    git clone --recurse-submodules https://github.com/terilenard/dias-hackathon-testbed1.git 

.. code-block:: bash
 
    cd dias-hackathon-testbed1
    
If you completed those steps, you can start to install the modules, one at the time, in the following order.
    
1.2.1 VCAN0 Service
-------------------

First of all, several dependencies must be installed and compile by running several scripts.

.. code-block:: bash

   cd toolchain/scripts
  

   
Setup the virtual vcan bus using the following script:

.. code-block:: bash

   ./vcan.sh

Paths:

* Service: **/etc/systemd/network**
* Module: **/etc/modules-load.d**
* Bin file: **/bin/vcan.sh**

You can uset **ifconfig** after to test if the setup script ran successfully. **vcan0** should be visible and available also after reboot.

.. code-block:: bash
   
   ifconfig
   
1.2.2 CAN2UDP Service
---------------------

To set up *CAN2UDP* service, you need to run it with several arguments:

1. *local_port* : the local port on which it listens from external connections
2. *remote_ip* : the remote ip on which to bind to create bidirectional communication
3. *remote_port* : the remote port coresponding to the remote ip on which to connect

Example:

.. code-block:: bash

   ./can2udp.sh 6000 192.168.1.5 6001
   
Paths:

* Service: **/etc/systemd/system/can2udp.service**
* Bin file: **/usr/local/bin/can2udp**


1.2.3 IBMTSS Service
--------------------

This service installs the tss2 dependencies for the virtual tpm, and creates two services: the one for the tpm resource manager (tpm2-abrmd.service) and the virtual tpm service (ibmtss.service).

.. code-block:: bash

   ./tss.sh
   
Paths:

* Service tpm2-abrmd: **/etc/systemd/system/tpm2-abrmd.service**
* Config tpm2-abrmd: **/etc/dbus-1/system.d/tpm2-abrmd.conf**
* Service ibmtss: **/etc/systemd/system/ibmtss.service**
* Bin file ibmtss: **/usr/bin/tpm_server**

1.2.4 Logging Service
---------------------

.. code-block:: bash

   ./logging.sh
   
Paths:

* Service: **/etc/systemd/system/tpm2-abrmd.service**
* Config: **/etc/dias-logging/**
* Sources: **/usr/lib/python3/dist-packages/dias-logging**
* Logs: **/var/log/dias-logging/**

   
1.2.5 Firewall/IDS Service
--------------------------

.. code-block:: bash

   ./firewall.sh
   
1.2.6 Kuksa.val
---------------

.. code-block:: bash

   ./vss.sh
   
and

.. code-block:: bash

   ./kuksa.val.sh
  

1.3 Misc
--------

1.3.1 Increase RaspberryPi SWAP
-------------------------------


Temporary turn off swapping:

.. code-block:: bash

   sudo dphys-swapfile swapoff


Edit as root in **/etc/dphys-swapfile** the variable **CONF_SWAPSIZE**:

.. code-block:: bash

   CONF_SWAPSIZE=1024

.. code-block:: bash

   sudo nano /etc/dphys-swapfile


Initialize and turn on swapping

.. code-block:: bash

   sudo dphys-swapfile setup


.. code-block:: bash
   
   sudo dphys-swapfile start

