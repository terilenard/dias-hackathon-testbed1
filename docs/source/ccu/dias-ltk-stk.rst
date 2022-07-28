8. LTK-STK Master
=================


.. note::
  The Master configuration is similar to the one of the Slave. There are only minor differences, but they       matter. This page should be followed in parallel with the one that describe the Slave configuration.
  
8.1 Requirements
----------------

* Mosquitto configured
* CAN interfaces configured
* Configured and install TPM and TPM dependencies (tpm2_tss, tpm2_tools)

8.2 Instalation
---------------

At the moment there isn't a instalation script for this module.

Below is the directory structure used by dias-ltk-stk and the steps done to bootstrap keys. The directory structure must be created before bootstrapping. Similarly, the slave on ECU must have its directory structure created. Follow the steps below in parallel with the steps described in slave description. They are basically the same, only things like hostname and possibly directory names differ.

Boostrapping directory, make sure to create *MASTER_TPMCTX* directory first:

.. code-block:: bash

    cd dias-hackathon-testbed1/modules/dias-ltk-stk/src/
    
The following directory structure and files are used by the dias-ltk-stk service to manage long and short term keys:
 
 .. code-block:: bash
 
    MASTER_TPMCTX/
    ├── ASYMKEYCTX
    │   ├──KDISTROKEYS // LTK structures, delete to make master run LTK
    │   │   ├──pkextenc1.dat
    │   │   ├──pkprim_loaded1.dat
    │   │   ├──pkprim_pubenc1.dat
    │   │   ├──pkprim_sensenc1.dat
    │   │   └── sign1.dat
    │   ├── loadedk.ctx // Loaded context for master pub/priv keys
    │   ├── MHMACKEYS
    │   ├── prvk.ctx // Private key
    │   └── pubk.ctx // Public key
    ├── EXTKEYSTORE
    │   ├── extkey1.ctx // Loaded context for Slave public key
    │   ├── extkey.ctx // Slave public key
    └── primary.ctx


To start bootstrapping *cd* in *MASTER_TPMCTX*:

.. code-block:: bash
 
    mkdir MASTER_TPMCTX ; cd MASTER_TPMCTX
    
Create the above directory structure:

.. code-block:: bash

    mkdir MASTER_TPMCTX/ASYMKEYCTX ; \
    mkdir MASTER_TPMCTX/ASYMKEYCTX/KDISTROKEYS ; \
    mkdir MASTER_TPMCTX/ASYMKEYCTX/HMACKEYS ; \
    mkdir MASTER_TPMCTX/EXTKEYSTORE
    
Now that we have the directory structure, we can run the following commands from *MASTER_TPMCTX* directory. First create the *primary.ctx*:

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
 
      scp ASYMKEYCTX/pubk.ctx pi@192.168.1.129:/home/pi/dias-hackathon-testbed1/modules/dias-ltk-stk/src/MASTER_TPMCTX/EXTKEYSTORE/extkey.ctx
   
.. note::
    This can only be done if the ECU Slave dias-ltk-stk service the directory structure created. The Master       needs the Slave public key, and the Slave need the Master public key
      
The dias-ltk-stk service should look like this:

.. code-block:: bash

    [Unit]
    Description=DIAS Key Manager Slave Service
    After=mosquitto.service
    Requires=mosquitto.service

    [Service]
    WorkingDirectory=/home/pi/dias-hackathon-testbed1/modules/dias-ltk-stk/src
    Type=simple
    ExecStart=/usr/bin/python3 /home/pi/dias-hackathon-testbed1/modules/dias-ltk-stk/src/master_kmngr.py -c /home/pi/dias-hackathon-testbed1/modules/dias-ltk-stk/src/config/master_kmngr.ini
    User=pi
    Group=pi

    [Install]
    WantedBy=multi-user.target


And the config file like this:

.. code-block:: bash

    [Log]
    level=debug
    filename=/var/log/dias-ltk-stk/master_kmngr.log
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
    ext_pub_key=MASTER_TPMCTX/EXTKEYSTORE/extkey.ctx

    [CAN]
    ; CAN name
    vbus=can1
    bitrate=500000
    ;LTK CAN id
    ltk_st=0xff100
    ;STK CAN id
    stk_st=0xff200

    [mqtt]
    user=master_kmngr
    passwd=master_kmngr
    host=127.0.0.1
    port=1883
