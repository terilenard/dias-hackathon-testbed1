MixCAN Master
=============

MixCAN master authenticates or verifies data framse based on its configuration. It monitors a set of CAN IDs and verifies authentication tags for it. It leverages the same short term symmetric key (STK) periodically received from the LTK-STK Slave service via mqtt as the MixCAN slave. 

Repository: https://github.com/terilenard/dias-mixcan

.. node::
  The instalation is similar to the MixCAN Slave one. Very little differs.
  
  
Requirements
------------

* Configured mosquitto mqtt broker
* Configured dias-ltk-stk key manager


Installation
------------

To install mixcan run the script *from *toolchain/scripts/* :

.. code-block:: bash

    ./mixcan.sh r
    
The *mixcan.service* should look like this:

.. code-block:: bash

    [Unit]
    Description=Mixcan Module

    [Service]Type=simple
    ExecStart=/usr/bin/python3 /usr/lib/python3/dist-packages/mixcan/manager.py -c /etc/mixcan/config.ini
    User=pi
    Group=pi

    [Install]
    WantedBy=multi-user.target
    
And the */etc/mixcan/config.ini* should look like this:

.. code-block:: bash

    [mqtt]
    user = mixcan
    passwd = mixcan
    host = 127.0.0.1
    port = 1883

    [key]
    last_key = /etc/mixcan/keys/last_key.dat

    [mixcan]
    is_sender = False
    frame_id = 0x11 0x12 0x13
    mixcan_id =  0x21 0x22 0x23

    [pycan]
    can =can1

    [log]
    path = /var/log/mixcan/mixcan.log
    
where *is_sender* enables the service to send authenticated frames, *frame_id* is a sequence of CAN frame ids that are monitored, and *mixcan_id* is a list with a coresponding set of CAN frame ids authentication tags.

.. node::
  The *frame_id* and *mixcan_id* lists should be the same ones as those configured on the MixCAN Slave on the ECU.
  

