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

    sudo apt install -y git can-utils net-tools


3.3 Connect to a CAN bus
------------------------
