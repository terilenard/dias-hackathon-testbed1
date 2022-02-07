.. DIAS Hackathon Testbed-1 documentation master file, created by
   sphinx-quickstart on Wed Dec 15 08:55:21 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DIAS Hackathon Testbed-1's documentation!
====================================================

The current page serves as the official documentation developed by UMFST (University of Medicine, Pharmacy, Science and Technology of Targu Mures), as part of the 
DIAS (Diagnostic Anti-Tampering Systems) H2020 project.

This documentation describes how to configure the Testbed-1 for the `Hackathon <https://dias-project.com/Hack-a-Truck>`_  2 event, organized by DIAS. Here, you can find information on how to configure, install the testbed, and how to connect and interact with it. The first part of the documentation (Section 1 and 2) is intended to those who need to configure the testbed. The second part (Section 3) is intended to users who want to interact with the system.

The system consist in three main components. First, a in-vehicle machine (Virtual Machine or RaspberryPi) simulating the vehicle network. The second one, is a cloud machine in which several services run that collect data published by the in-vehicle machine. And thirdly, a *hacker* machine that wants to compromise the network communication in the in-vehicle network. 


Interacting with the Testbed
````````````````````````````

There are two main ways to interact with the tesbed, depending on how the in-vehicle machine is installed. If the in-vehicle machine is directly connected to a physical CAN bus, then the participants (hackers) can connect directly to the CAN bus and listen/sent messages. Alternatively, if the in-vehicle machine is configured as a Virtual Machine, it will expose two UDP ports, on which only one participant can connect and interact with the CAN bus.

For the second option, Section 3 describes how to install and configure a Ubuntu Virtual Machine that can connect via a `can2udp <https://opensource.lely.com/canopen/docs/can2udp/>`_ service to the in-vehicle machine. 

In-Vehicle and Cloud
````````````````````
For those interested in finding more details to how the testbed is configure, and are interested to dive deeper in the configuration process, there are two additional documentation made available by the DIAS partners:

* `Getting Started with DIAS-KUKSA <https://dias-kuksa-doc.readthedocs.io/en/latest/>`_
* `DIAS UMFST How To’s documentation <https://dias-kuksa-firewall-doc.readthedocs.io/en/latest/index.html>`_

In this setup, for each component a separate automated script was made to ease the installation process. This means, that the dependencies and instalation process is not described step by step, but it points out what to run in order to install a specific component.

For all three setups, the following repository is used `DIAS Hackathon Testbed-1 Github <https://github.com/terilenard/dias-hackathon-testbed1>`_


.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   iothub
   invehicle
   participant



Acknowledgement
---------------

This work was funded by the European Union’s Horizon 2020 Research and Innovation Programme through DIAS project under Grant Agreement No. 814951. 
This document reflects only the author’s view and the Agency is not responsible for any use that may be made of the information it contains

Authors
-------

Authors can be found and contacted on: **https://nislab.umfst.ro/**
