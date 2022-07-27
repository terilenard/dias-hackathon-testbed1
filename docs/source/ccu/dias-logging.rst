7. Logging
==========
The Logging service generates secure logs using the Trusted Platform Module (TPM). It uses the digital signature engine of the TPM, together with the Platform Configuration Registers (PCRs) to secure logs. The service receives log alerts from all security module configured on the CCU via MQTT.

7.1. Requirements
-----------------

* Configured and install TPM and TPM dependencies (tpm2_tss, tpm2_tools)
* MQTT broker Mosquitto

7.2 Instalation
---------------

Navigate to *toolchain/scripts/* and execute the install script:

.. code::

    ./logging.sh
    

7.3. Bootstrapping
------------------

After instalation, the service is not ready to be run. The service requires a set of key generated with the TPM. The keys must be generated inside the directory */etc/tpm_handlers/dias-logging*:

.. code::

  cd /etc/tpm_handlers/dias-logging/

Before generating the keys, a primary TPM object must be created:

.. code::

  tpm2_createprimary primary.ctx
  
Once this is done, to generate a pair of keys run the command below:
 
.. code::
  
    tpm2_create -C primary.ctx -u key.pub -r key.priv
  
To verify the keys, you can try to load them into the TPM:
  
.. code::
  
      tpm2_load -C primary.ctx -u key.pub -r key.priv -c  key.ctx
        
After the keys were generated, you should restart the *dias-logging* service:

.. code::

        sudo systemctl restart dias-logging.service
   
