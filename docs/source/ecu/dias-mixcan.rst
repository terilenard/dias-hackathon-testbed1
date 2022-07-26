MixCAN Slave
============

MixCAN slaves acts authenticates data framse based on its configuration. It monitors a set of CAN IDs and computes authentication tags for it. It leverages a short term symmetric key (STK) periodically received from the LTK-STK Slave service via mqtt. In the figure below it can be seen how MixCAN works, assuming that on the ECU there is a program that is executed to simulate CAN traffic (canplayer), mixcan will act as a gateway between the two CAN networks forwarding all the frames together with their authentication tags.

.. image:: /mixcan-vcan-can.PNG
  :width: 1200
  :alt: MixCAN

Repository: https://github.com/terilenard/dias-mixcan

Requirements
------------

* Configured mosquitto mqtt broker
* Configured dias-ltk-stk key manager


Installation
------------

To install mixcan run the script *from *toolchain/scripts/* :

.. code-block:: bash

    ./mixcan.sh s
    
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
    is_sender = True
    frame_id = 0x11 0x12 0x13
    mixcan_id =  0x21 0x22 0x23

    [pycan]
    can =can1

    [log]
    path = /var/log/mixcan/mixcan.log
    
where *is_sender* enables the service to send authenticated frames, *frame_id* is a sequence of CAN frame ids that are monitored, and *mixcan_id* is a list with a coresponding set of CAN frame ids authentication tags.
