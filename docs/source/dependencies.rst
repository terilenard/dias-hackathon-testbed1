Testbed dependencies
====================

Each component in the testbed has several dependencies. This document describes what dependencies are necessary to be installed in order to configure other modules.


Preliminaries
`````````````
Run a update:

.. code-block:: bash

    sudo apt update && sudo apt upgrade

Install git:

.. code-block:: bash

    sudo apt install git

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
    
The *vcan0* interface should be visable in *ip link*:

.. code-block:: bash
 
    ip link

To setup the can interface with the MCP2515 controller you need to modify the boot.config file on your image, and copy the dt overlay file:

.. code-block:: bash

    cd toolchain/utils/rpi3-mcp2515/
    
Copy *boot/config.txt* file

.. code-block:: bash

    sudo cp config.txt /boot/config.txt

Copy dt overlay:


Trusted Platform Module Configuration
`````````````````````````````````````

Both the *ECU* and *CCU* require the *tpm2-tss* libraries and the *tpm2-tools* utilities. The *tss.sh* script installs the required TPM2 dependencies together with the TPM2-ABRMD resource manager. This script will also compile and install IBM's Virtual TPM. If you have a physical TPM2, there are below some command that will help you disable IBM Virtual TPM and use the dedicated one instead.

The install script is located in *toolchain/scripts*. From there you can execute:

.. code-block:: bash

    ./tss.sh
    
Compared to a physical TPM, which is exposed as a linux device, the virtual TPM exposes socket which allows similar interactions with it. Next, we must configure the TPM resource manager (tpm2-abrmd) to connect to the port opened by the tpm_server, and not to the default _/dev/tpm0_ device. This requires some changes on the tpm2-abrmd service unit.

If you followed a similar configuration with the one in this guide, the service file should be located in `/usr/local/lib/systemd/system/tpm2-abrmd.service`.

.. code-block:: bash

        [Unit]                                          
        Description=TPM2 Access Broker and Resource Management Daemon        
        # These settings are needed when using the device TCTI. If the        
        # TCP mssim is used then the settings should be commented out.        
        - After=dev-tpm0.device
        + #After=dev-tpm0.device
        - Requires=dev-tpm0.device
        + #Requires=dev-tpm0.device
        [Service]
        Type=dbus                                                                                                                                                               BusName=com.intel.tss2.Tabrmd                                                                                                                                           - ExecStart=/usr/local/sbin/tpm2-abrmd
        + ExecStart=/usr/local/sbin/tpm2-abrmd --tcti=mssim:host=localhost,port=2321
        User=tss
        [Install]                                                                                                                                                               WantedBy=multi-user.target  


After modifying the file, we must reload the service using:

.. code-block:: bash

        sudo systemctl daemon-reload

Last but not least, *cd* to the *tpm2-abrmd* downloaded repository and move the following file so the *tss* can access the dbus:

.. code-block:: bash

        sudo cp dist/tpm2-abrmd.conf /etc/dbus-1/system.d/tpm2-abrmd.conf 

the tpm2-abrmd.conf should look like this:

.. code-block:: bash
        <busconfig>
          <policy user="tss">
            <allow own="com.intel.tss2.Tabrmd"/>
          </policy>
          <policy user="root">
            <allow own="com.intel.tss2.Tabrmd"/>
          </policy>
          <policy context="default">
            <allow send_destination="com.intel.tss2.Tabrmd"/>
            <allow receive_sender="com.intel.tss2.Tabrmd"/>
          </policy>
        </busconfig>

Change the /dev/tpm0 ownership to tss:

.. code-block:: bash

        sudo chown tss:tss /dev/tpm0

Now, we can restart the *tpm2-abrmd* and he will try to connect on port *2321* on *localhost* to a virtual tpm.


MQTT Broker - Mosquitto
``````````````````````

