LTK-STK Slave
=============

Requirements
------------

* Mosquitto configured
* CAN interfaces configured

Instalation
-----------

At the moment there isn't a instalation script for this module.


Below is the directory structure used by dias-ltk-stk and the steps done to bootstrap keys. The directory structure must be created before bootstrapping. Similarly, the master on CCU must have its directory structure created. Follow the steps below in parallel with the steps described in master description. They are basically the same, only things like hostname and possibly directory names differ.

Boostrapping directory, make sure to create *SLAVE_TPMCTX* directory first:

.. code-block:: bash

    cd dias-hackathon-testbed1/modules/dias-ltk-stk/src/SLAVE_TPMCTX/
    
The following directory structure and files are used by the dias-ltk-stk service to manage long and short term keys:
 
 .. code-block:: bash
 
    SLAVE_TPMCTX/
    ├── ASYMKEYCTX
    │   ├── KDISTROKEYS
    │   ├── loadedk.ctx // Context object of loaded pub/priv keys
    │   ├── MHMACKEYS
    │   ├── prvk.ctx // Private key
    │   └── pubk.ctx // Public key 
    ├── EXTKEYSTORE
    │   ├── extkey2.ctx // Loaded context object for Master public key
    │   ├── extkey.ctx // External public key of Master
    │   ├── tpmdecf1.dat // Decrypted STK from Master
    │   ├── tpmsigdata1.dat // Encrypted STK with LTK
    │   └── tpmsigsig1.dat // Digital signature for STK with LTK
    └── primary.ctx

To start bootstrapping *cd* in *SLAVE_TPMCTX*:

.. code-block:: bash
 
    cd SLAVE_TPMCTX
    
First create the *primary.ctx*:

.. code-block:: bash
 
    tpm2_createprimary -c primary.ctx 
    
Create the master public and private keys, if this step is repeated and other key pair is generated, then the master public part needs to be copied on the slave:

.. code-block:: bash
 
    tpm2_create -C primary.ctx -u ASYMKEYCTX/pubk.ctx -r ASYMKEYCTX/prvk.ctx -c ASYMKEYCTX/loadedk.ctx
    

After *tpm2_create* the key is already loaded into the TPM, if you want to manually load the key run the next command:

.. code-block:: bash
 
    tpm2_load -C primary.ctx -u ASYMKEYCTX/pubk.ctx -r ASYMKEYCTX/prvk.ctx -c ASYMKEYCTX/loadedk.ctx


Lastly, the public key of the Slave must be copied on the Master, be careful so that the working directory on the slave is created:
 
.. code-block:: bash
 
      scp ASYMKEYCTX/pubk.ctx pi@192.168.1.237:/home/pi/dias-hackathon-testbed1/modules/dias-ltk-stk/src/SLAVE_TPMCTX/EXTKEYSTORE/extkey.ctx
      
      
The dias-ltk-stk service should look like this:

.. code-block:: bash

    [Unit]
    Description=DIAS Key Manager Slave Service
    After=mosquitto.service
    Requires=mosquitto.service

    [Service]
    WorkingDirectory=/home/pi/dias-hackathon-testbed1/modules/dias-ltk-stk/src
    Type=simple
    ExecStart=/usr/bin/python3 /home/pi/dias-hackathon-testbed1/modules/dias-ltk-stk/src/slave_kmngr.py -c /home/pi/dias-hackathon-testbed1/modules/dias-ltk-stk/src/config/slave_kmngr.ini
    User=pi
    Group=pi

    [Install]
    WantedBy=multi-user.target


And the config file like this:

.. code-block:: bash

    [Log]
    level=debug
    filename=/var/log/dias-ltk-stk/slave_kmngr
    maxBytes=1048576
    backupCount=2 

    [Secrets]
    ; The shared secret between the local components - used to exchange encrypted secrets amongst local components
    shared_secret=!23gAb9_4op;Lqt12562123456789012

    ; The size of LTK (long-term keys)
    ltk_size=256

    ; The size of STK (short-term keys)
    stk_size=128
    ; The public key file of the external recipients (at the moment only one is supported!)
    ext_pub_key=SLAVE_TPMCTX/EXTKEYSTORE/extkey.ctx

    [CAN]
    ; CAN name
    vbus=can1
    bitrate=500000
    ;LTK CAN id
    ltk_st=0xff100
    ;STK CAN id
    stk_st=0xff200

    [mqtt]
    user=slave_kmngr
    passwd=slave_kmngr
    host=127.0.0.1
    port=1883
