Testbed dependencies
====================

Each component in the testbed has several dependencies. This document describes what dependencies are necessary to be installed in order to configure other modules.


Preliminaries
`````````````
Run a update:

.. code-block:: bash

    sudo apt update && sudo apt upgrade
    
Have a local copy of the repository:

.. code-block:: bash
 
    git clone --recursive https://github.com/terilenard/dias-hackathon-testbed1.git
    
To update the local copy, you can run the following command from the project root directory:

.. code-block:: bash
 
    git submodule update --init –recursive
    
In the project, there is a *toolchain* directory that contains scripts that can be used to install dependencies and modules. In the *dependencies* directory, there are linked the libraries used in the testbed.


Controller Area Network Configuration
`````````````````````````````````````
The current section describes the Controller Area Network (CAN) configuration required for each component.

Electronic Control Unit
+++++++++++++++++++++++

Requirements:

* MCP2515 CAN controller with TJA1050 CAN Transceiver
* One virtual CAN (vcan)
* One physical CAN (can1/can0)

To setup vcan go to project root:

.. code-block:: bash
 
    cd dias-hackathon-testbed1

Run the setup script for vcan:

.. code-block:: bash
 
    cd toolchain/scripts
    
Install can-utils:

.. code-block:: bash

    sudo apt install can-utils

The following script will create a *vcan0* interface and will configure it to be up on boot:

.. code-block:: bash
 
    ./vcan.sh

To setup the can interface with the MCP2515 controller you need to modify the boot.config file on your image, and copy the dt overlay file:

.. code-block:: bash

    cd toolchain/utils/rpi3-mcp2515/
    
Copy *boot/config.txt* file

.. code-block:: bash

    sudo cp config.txt /boot/config.txt

Copy dt overlay:


Trusted Platform Module Configuration
`````````````````````````````````````


MQTT Broker - Mosquitto
``````````````````````

