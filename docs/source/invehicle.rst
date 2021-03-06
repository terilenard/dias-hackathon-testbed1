1. In Vehicle Setup
===================

This page describes how to setup the In Vehicle machine. The github project contains a dedicated directory named **toolchain** where a directory containing setup scripts exists.
Those scripts are meant to install dependencies, compile required libraries, and install modules. Those scripts run both, root and non-root commands. The scripts should be run
as normal user. If a script needs to run a command as root, it will ask at one point for the root password. As such, do not run the scripts as root. The scripts are meant to automate the install process and should be run in the order mentioned below. Some may take a longer time to run, since compilation of some libraries take time. 

The In-Vehicle setup is meant to simulate a Controller Area Network (CAN) system inside a linux based system. Inside the linux box a virtual CAN (vcan) is used to simulate the CAN bus. Each component connects to this CAN bus to listen or exchange messages.



1.1 Requirements
----------------

The In-Vehicle machine can be configured on one of the following systems:

1. Ubuntu Virtual Machine. Version: Ubuntu 20.04.3 live server amd64
2. RaspberryPi 4. Version: RaspberryPi OS (old Raspbian)

System requirements:

* 8GB RAM memory
* Minimum 64GB storage space
* 4 CPU cores
* Network Interface in Bridge mode (ONLY for Virtual Machine)
* Increased SWAP size (ONLY for RaspberryPi's that have less then 8GB of RAM)

If the testbed is configured for option 1, then the *CAN2UDP* service must be installed, to allow user to connect to the virtual CAN bus from exterior, withtout having direct access to the software running in the linux box. If option 2 is chosen, then the *CAN2UDP* service is optional, but a additional *CANGW* service must be install so that the traffic from the virtual can is forwarded to the CAN bus connected to the RaspberryPi, and vice-versa.

Modules list:

* VCAN0 - RaspberryPi (Required), Ubuntu VM (Required)
* CAN-Player - RaspberryPi (Required), Ubuntu VM (Required)
* IBMTSS-VTPM - RaspberryPi (Required), Ubuntu VM (Required)
* LogPublisher - RaspberryPi (Required), Ubuntu VM (Required)
* Firewall/IDS -  RaspberryPi (Required), Ubuntu VM (Required)
* DBC-FeederSec - RaspberryPi (Required), Ubuntu VM (Required)
* Kuksa.val/VSS  -  RaspberryPi (Required), Ubuntu VM (Required)
* SecOC -  RaspberryPi (Required), Ubuntu VM (Required)
* Data Delivery Controller - RaspberryPi (Required), Ubuntu VM (Required)
* CloudFeeder-Sec - RaspberryPi (Required), Ubuntu VM (Required)
* CAN2UDP - RaspberryPi (Optional), Ubuntu VM (Required)
* CANGW - RaspberryPi (Required), Ubuntu VM (Optional)

Depending on the Tesbed configuration, the modules marked as *Required* should be installed. To do so, follow the instructions bellow for each specific module.

Before starting the actual installation, be sure to update your machine, and download the respository.

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
    
.. code-block:: bash

   cd toolchain/scripts
    
If you completed those steps, you can start to install the modules, one at the time, in the following order. Also, you can skip optional modules for your configuration.

   
   
1.2 VCAN0 Service
^^^^^^^^^^^^^^^^^

The **VCAN0** service is meant to create on startup the virtual CAN (vcan0) bus, and to keep it alive. 
   
Setup the virtual vcan bus using the following script:

.. code-block:: bash

   ./vcan.sh

Paths:

* Service: **/etc/systemd/network**
* Module: **/etc/modules-load.d**
* Bin file: **/bin/vcan.sh**

You can use **ifconfig** after to test if the setup script ran successfully. **vcan0** should be visible and available also after reboot.

.. code-block:: bash
   
   ifconfig
   
1.3 CAN2UDP Service
^^^^^^^^^^^^^^^^^^^

The *CAN2UDP* service is mandatory for the virtual box setup, but optional for the board setup. This service uses two UDP ports to create a bidirectional communication to another *CAN2UDP* service. By doing this, two CAN interfaces (two virtual CAN interfaces) can be linked together even if they are installed on different machines. *CAN2UDP* will take care that both remote CAN busses are synchronized, and frames that are sent on a local virtual bus, are also available to the remote one.

To connect from a different machine to this service, pleace check Section 3 of this documentation. For this service to run properly, we advice to use static IP addresses, since the service needs to know where to connect, on which port, and vice-versa, the participant needs to know the IP and port of the service.

To set up *CAN2UDP* service, you need to run it with several arguments:

1. *local_port* : the local port on which it listens for incomming packets
2. *remote_ip* : the source IP address from which it accepts packets
3. *remote_port* : the source port from which it accepts packets

Example:

.. code-block:: bash

   ./can2udp.sh 6000 192.168.1.5 6001
   
Here, you should change the ports and the IP according to your network configuration.

Paths:

* Service: **/etc/systemd/system/can2udp.service**
* Bin file: **/usr/local/bin/can2udp**


1.4 IBMTSS Service
^^^^^^^^^^^^^^^^^^

The *IBMTSS* service runs a virtual Trusted Platform Module. It is used by the Logging service to sign log messages. The install script compiles the tss2 library, the tpm2-tools, the actual virtual TPM, and creates two services: one for the TPM resource manager (tpm2-abrmd.service) and the virtual TPM service (ibmtss.service). This script may take a little more time to finish.

.. code-block:: bash

   ./tss.sh
   
Paths:

* Service tpm2-abrmd: **/etc/systemd/system/tpm2-abrmd.service**
* Config tpm2-abrmd: **/etc/dbus-1/system.d/tpm2-abrmd.conf**
* Service ibmtss: **/etc/systemd/system/ibmtss.service**
* Bin file ibmtss: **/usr/bin/tpm_server**

Note: If you receive a *error DA lockout mode* in the *ibmtss* service, run the following command and restart the service:

.. code-block:: bash

   tpm2_dictionarylockout --setup-parameters --max-tries=4294967295 --clear-lockout


1.5 Logging Service
^^^^^^^^^^^^^^^^^^^

This *Logging* service uses the *IBMTSS* service to generate signature for events generate by the *Firewall/IDS* service. 

.. code-block:: bash

   ./logging.sh
   
Paths:

* Service: **/etc/systemd/system/tpm-logger.service**
* Config: **/etc/dias-logging/**
* Sources: **/usr/lib/python3/dist-packages/dias-logging**
* Logs: **/var/log/dias-logging/**

   
1.6 Firewall/IDS Service
^^^^^^^^^^^^^^^^^^^^^^^^^^

The Firewall (FW) and IDS (Intrusion Detection System) basically function on the same **Rule Processing Engine** (denoted in the following as RPE). Depending on how the rules are written in it's associated **rule file**, the RPE will function as a Stateful Firewall, analyzing sequences of CAN frames based on their identifier field, or as a Intrusion Detection System, by performing a byte-level inspection in the CAN frame data field.

To install the *Firewall/IDS* and helper services run the script bellow:

.. code-block:: bash

   ./firewall.sh
   
1.6.1 Helper processes
^^^^^^^^^^^^^^^^^^^^^^

The Firewall/IDS process uses several additional helper processes. 

1. Pycan: a process that listens to a CAN interface (e.g. vcan0, /dev/can0), reading incomming frames, extracting their ID and DATA field, and then forwarding the preprocessed data, via a named pipe, to the Firewall/IDS process. The named location of the named pipe can be set in the configuration file, described in the next section.

2. Log Publisher: monitors the logs produced by the FW/IDS and publishes them via MQTT to Data Delivery Controller


1.6.2 Configuration
-----------------

A configuration file is used by the Firewall/IDS process to store a set of parameters. The configuration file named *diasfw.cfg*, and can be found in */etc/diasfw/*. It contains the followings:

* *ruleFile* : the location of the XML file, containing the Firewall/IDS set of rules.
* *secureLog* : boolean value under the form of a string. If *"true"* the process will leverage the Secure Logging process to generate signed logs. Else, if it is *"false"* the logs are saved  (file logging, syslog?).
* *canPipe*: path to a named piped used to communicate with a helper process that reads and preprocesses CAN frames. 
* *tpmPipe*: path to a named pipe used to communicate with the Secure Logging process.

The pycan configuration file *config.py* is located in */etc/diasfw/*. The parameters of interest are the following:

* *PIPE_PATH* : path to a named piped used to communicate with the Firewall/IDS
* *CAN_CHANNEL_REC* : the process will listen for CAN interface on this interface. If a combination of physical interface and virutal interface was chosen than the value for this parameter should be the physical interface (e.g., CAN0). 
* *CAN_CHANNEL_SEND* : the process will forward the incomming frames to this interface. For the current demo those frames will not be used. If a combination of physical interface and virutal interface was chosen than the value for this parameter should be the virtual interface (e.g., VCAN0), else if a combination of two  virutal interfaces was chosen than the value for this parameter should be VCAN1.
* *LOGFILE* : the location of the pycan log file.

In order to be able to publish data to the Bosch IoT Hub, the Log Publisher process requires several parameters:

* username: MQTT user
* password: MQTT password.
* host: Host for the MQTT broker.
* port: Port for the MQTT broker.
* log_file: Path to the FW/IDS log file (/var/log/diasfw/diasfw.log).

   
1.7 Kuksa.val
^^^^^^^^^^^^^

.. code-block:: bash

   ./vss.sh
   
and

.. code-block:: bash

   ./kuksa.val.sh
  

1.8 Data Delivery Controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.9 DBCFeeder-Sec
^^^^^^^^^^^^^^^^^

1.10 Autosar SecOc
^^^^^^^^^^^^^^^^^^

1.11 CloudFeeder-sec
^^^^^^^^^^^^^^^^^^^^

1.12 Bosch Preporcessor
^^^^^^^^^^^^^^^^^^^^^^^

0 Misc
--------

0.1 Increase RaspberryPi SWAP
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

