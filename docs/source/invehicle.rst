1. In Vehicle Setup
===================

This page describes how to setup the In Vehicle machine. The github project contains a dedicated directory named **toolchain** where a directory dedicated to setup scripts exists.
Those scripts are meant to install dependencies, compile required libraries, and install modules. Those scripts run both, root and non-root commands. The scripts should be run
as normal user. If a script needs to run a command as root, it will ask at one point for it. The scripts are meant to automate the install process and should be run in the order
mentioned below. Some may take a longer time to run, since compilation of some libraries take time. 

1.1 Requirements
----------------

1. Raspberry Pi 4 (recommended) with Rasbian

2. Ubuntu virtual machine.

System requirements for Ubuntu virtual machine: minimum 30gb storage and 5gb RAM memory.

1.2 Dependencies
---------

.. code-block:: bash

   sudo apt -y update

.. code-block:: bash

    sudo apt install -y git python3-pip net-tools
   
.. code-block:: bash
 
    mkdir Workspace ; cd Workspace
    
.. code-block:: bash

    git clone --recurse-submodules https://github.com/terilenard/dias-hackathon-testbed1.git 

.. code-block:: bash
 
    cd dias-hackathon-testbed1
    
1.2.1 VCAN0 Service
-------------------

First of all, several dependencies must be installed and compile by running several scripts.

.. code-block:: bash

   cd toolchain/scripts
   
Setup the virtual vcan bus using the following script:

.. code-block:: bash

   ./vcan.sh

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

1.2.3 IBMTSS Service
--------------------

This service installs the tss2 dependencies for the virtual tpm, and creates two services: the one for the tpm resource manager (tpm2-abrmd.service) and the virtual tpm service (ibmtss.service).

.. code-block:: bash

   ./tss.sh

1.2.4 Logging Service
---------------------

.. code-block:: bash

   ./logging.sh
   
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
  
