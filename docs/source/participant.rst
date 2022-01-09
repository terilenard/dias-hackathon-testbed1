3. User Setup
===================

This section describes how users should setup their machine in order to interact with the Testbed1. The following configuration was tested on a Ubuntu 20.04 LTS virtual machines.

3.1 Requirements
----------------

1. A Ubuntu or Debian based OS.

2. If the In-Vehicle system is a virtual machine, please follow Section 3.2. Otherwise follow Section 3.3.

3.2 Connect to Virtual Vehicle
------------------------------

First, please install *git* to download the repository with the setup scripts, *can-utils* to install a set of tools to test the CAN bus interface, and *net-tools* for networking verifications:

.. code-block:: bash

    sudo apt install -y git can-utils net-tools python3-pip

Clone the following repository and change directory to the setup scripts:


.. code-block:: bash

    git clone https://github.com/terilenard/dias-hackathon-testbed1.git 

.. code-block:: bash
 
    cd dias-hackathon-testbed1
    
If you completed those steps, you can start to install the modules, one at the time, in the following order.
   
.. code-block:: bash

   cd toolchain/scripts
   
1.2.1 VCAN0 Service
-------------------

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
   
1.2.2 CAN2UDP Service
---------------------

The *CAN2UDP* service is mandatory for user that want to connect to a virtualized In-Vehicle machine. This service uses two UDP ports to create a bidirectional communication to another *CAN2UDP* service. By doing this, two CAN interfaces (two virtual CAN interfaces) can be linked together even if they are installed on different machines. *CAN2UDP* will take care that both remote CAN busses are synchronized, and frames that are sent on a local virtual bus, are also available to the remote one.

For this service to run properly, we advice to use static IP addresses, since the service needs to know where to connect, on which port, and vice-versa, the participant needs to know the IP and port of the service.

To set up *CAN2UDP* service, you need to run it with several arguments:

1. *local_port* : the local port on which it listens from external connections
2. *remote_ip* : the remote ip on which to bind to create bidirectional communication
3. *remote_port* : the remote port coresponding to the remote ip on which to connect

Example:

.. code-block:: bash

   ./can2udp.sh 6001 192.168.1.4 6000
   
Here, you should change the ports and the IP according to your network configuration.

Paths:

* Service: **/etc/systemd/system/can2udp.service**
* Bin file: **/usr/local/bin/can2udp**

3.3 Connect to a CAN bus
------------------------
TODO
