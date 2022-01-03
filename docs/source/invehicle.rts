1. In Vehicle Setup
===============

This page describes how to setup the In Vehicle machine. The github project contains a dedicated directory named _toolchain_ where a directory dedicated to setup scripts exists.
Those scripts are meant to install dependencies, compile required libraries, and install modules. Those scripts run both, root and non-root commands. The scripts should be run
as normal user. If a script needs to run a command as root, it will ask at one point for it. The scripts are meant to automate the install process and should be run in the order
mentioned below. Some may take a longer time to run, since compilation of some libraries take time. 

1.1 Requirements
----------------

1. Raspberry Pi 4 (recommended) with Rasbian

2. Ubuntu virtual machine.

System requirements for Ubuntu virtual machine: minimum 30gb storage and 5gb RAM memory.

1.2 Setup
----------------

.. code-block:: bash

   sudo apt -y update

.. code-block:: bash

   sudo apt install -y git python3-pip
 
 .. code-block:: bash
 
    mkdir Workspace ; cd Workspace
    
 .. code-block:: bash

    git clone --recurse-submodules https://github.com/terilenard/dias-hackathon-testbed1.git 

 .. code-block:: bash
 
    cd dias-hackathon-testbed1
    
1.2.1 Dependencies

First of all, several dependencies must be installed and compile by running several scripts.

