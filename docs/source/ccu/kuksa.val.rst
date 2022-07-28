10. Kuksa.val Server
====================

10.1. Requirements
`````````````````

* MQTT broker Mosquitto for dbcfeeder and cloudfeeder

10.2. Instalation
`````````````````

Tun the script below from *toolchain/scripts*. This will compile the kuksa.val server and install it as a service:

.. code::

  ./kuksa.val.sh
  
  
11. SecOC and DBCFeeder
=======================

To setup the Secure On-Board Communication (SeOC) together with the Kuksa.val dbcfeeder run the script below from *toolchain/scripts*:

.. code::

    ./secoc.sh

.. note::

    After instalation you need to copy the *dias.dbc* to /etc/dbcfeeder/. If the .dbc file name differs, then change it in dbcfeeder configuration too.
    
.. note::

    SecOC counter.txt in */etc/dbcfeeder* must be configured manually. Similarly, the SecOC key must be hardcoded manually in secoc_verification.py.
    
 
12. Cloudfeeder
===============

To install the cloudfeeder service, run the script below from *toolchain/scripts*:

.. code::

    ./cloudfeeder.sh
    
13. Telemetry and Log Deliverers
================================

The Deliverers handle the communication between the CCU and the Cloud. Those services translate mqtt messages comming from different services (e.g., cloudfeeder, dias-logging) to HTTP messages that are published to the Bosch Iot Insights.

To install those services, run the script below from *toolchain/scripts*:

.. code::

    ./iotinsightsdelivery.sh
    
After you ran the script, each service must be configured manually with Bosch IoT Insights credentials. The source codes were installed in */usr/lib/node-modules/*.
 
13.1 Telemetry Deliverer Configuration
``````````````````````````````````````
 Go to the working directory:
 
.. code::

    cd /usr/lib/node-modules/telemetry-deliverer/
    
First create a *.env* file

.. code::
    
    touch .env
    
This is the configuration file for the service. It should look something like this:
 
.. code::

  MQTT_USERNAME=telemetry-deliverer
  MQTT_PASSWORD=telemetry-deliverer                                                                                                                                                                                                           
  INSIGHTS_USER=<bosch-iot-insights-api-user>                                                                            
  INSIGHTS_API_KEY=<bosch-iot-insights-api-key>

Afterwards, modify the *insightsConfig* variable in the *index.js* to took like this:

.. code::
  
  const insightsConfig = {
      user: process.env.INSIGHTS_USER ?? null,
      apiKey: process.env.INSIGHTS_API_KEY ?? null,
      url: process.env.INSIGHTS_URL ?? 'https://bosch-iot-insights.com/data-recorder-service/v2/',
      collection: process.env.INSIGHTS_COLLECTION ?? '<bosch-iot-collection-name>',
      project: process.env.INSIGHTS_PROJECT ?? '<bosch-iot-project-id>',
      type: process.env.INSIGHTS_METADATA_TYPE ?? 'testbed1',
  }; 
  
After this is done, you can restart the service:
 
.. code::
 
    sudo systemctl restart telemetry-deliverer
  
13.2 Log Deliverer Configuration
````````````````````````````````

 Go to the working directory:
 
.. code::

    cd /usr/lib/node-modules/log-deliverer/
    
First create a *.env* file

.. code::
    
    touch .env
    
This is the configuration file for the service. It should look something like this:
 
.. code::

  MQTT_USERNAME=log-deliverer
  MQTT_PASSWORD=log-deliverer                                                                                                                                                                                                           
  INSIGHTS_USER=<bosch-iot-insights-api-user>                                                                            
  INSIGHTS_API_KEY=<bosch-iot-insights-api-key>

Afterwards, modify the *insightsConfig* variable in the *index.js* to took like this:

.. code::
  
  const insightsConfig = {
      user: process.env.INSIGHTS_USER ?? null,
      apiKey: process.env.INSIGHTS_API_KEY ?? null,
      url: process.env.INSIGHTS_URL ?? 'https://bosch-iot-insights.com/data-recorder-service/v2/',
      collection: process.env.INSIGHTS_COLLECTION ?? '<bosch-iot-collection-name>',
      project: process.env.INSIGHTS_PROJECT ?? '<bosch-iot-project-id>',
      type: process.env.INSIGHTS_METADATA_TYPE ?? 'testbed1',
  }; 
  
After this is done, you can restart the service:
 
.. code::
 
    sudo systemctl restart log-deliverer
