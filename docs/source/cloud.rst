
2. Cloud Setup
==============

The cloud setup represents a virtual machine, running cloud services to which the in vehicle services publish information. Data is published by the mqtt client, will be received in the Bosch IoT Hub, where a Hono entry point exists. A Hono consumer will read the data from the hub, and saves it into a InfluxDB table. After that, Grafana reads the data saved into the database, and displays its content.

Usefull links:

* `DIAS Kuksa setup, Step 3: Cloud Setup <https://dias-kuksa-doc.readthedocs.io/en/latest/contents/cloud.html>`_
* `UMFST Cloud Setup <https://dias-kuksa-firewall-doc.readthedocs.io/en/latest/cloud.html>`_

Both links from above follow the same steps. You can have a look on them to find more details.

2.1 Requirements
----------------

To follow this page, several things are required:

* A Bosch IoT Hub subscription. If you don't have one a detailed guide on how to obtain one can be found `here <https://dias-kuksa-doc.readthedocs.io/en/latest/contents/cloud.html#bosch-iot-hub-as-hono>`_.
* A Ubuntu Virtual Machine.

and

.. code-block:: bash

  sudo apt update
  
.. code-block:: bash

  sudo apt install git
  
After git is installed, clone the testbed repository using:

.. code-block:: bash

  git clone https://github.com/terilenard/dias-hackathon-testbed1.git
  
The install scripts are locate in *dias-hackathon-testbed1/toolchain/scripts*:

.. code-block:: bash

  cd dias-hackathon-testbed1/toolchain/scripts

The scripts located here must be run as normal user, not root. If the script requires root rights, it will answer during runtime.
  
2.2 InfluxDB Setup
------------------

To install InfluxDB, together with its dependencies run:

.. code-block:: bash

  ./influx.sh


2.3 Grafana Setup
-----------------

Ubuntu setup of Grafana can be found `here <https://dias-kuksa-doc.readthedocs.io/en/latest/contents/cloud.html>`_ . The same steps are listed below for convenience:

.. code-block:: bash

  ./grafana.sh

Grafana can be access via a web browser on *http://<local-ip>:3000*. The default login username is *admin* and default login password is *admin*.

First off all, InfluxDB must be linked with Grafana. On the main page, select *Data Source* square, and click on the row associated with InfluxDB. Here the following fields must be set to:

* URL: http://localhost:8086
* DATABASE: dias_log
* User: admin
* Password: admin

and then Save.

To view the data saved in InfluxDB in Grafana, a new *Panel* must be created. 

To extract all logs, under *Query* tab, modify the query statement as **SELECT "time","value" FROM logs;**. 

After that modify in the *Panel Options*, on the left side of the editing page, the *Visualizations* style into *Logs*. This is set by default to *Time series*. 

Don't forget to save your changes by clicking *Apply*, on the top right button, after every step.

2.4 Hono Consumer Setup
-----------------------

The Hono consumer client is meant to read log data published to Bosch IoT Hub, and write it in Influxdb. The client can be installed and compiled manually, or via a Docker.

Manual setup:

.. code-block:: bash

    git clone https://github.com/terilenard/dias-cloud-umfst.git 

    cd dias-cloud-umfst/Consumer

    mvn clean package -DskipTests  # Build the project

    java -jar target/maven.consumer.hono-0.0.1-SNAPSHOT.jar --hono.client.tlsEnabled=true --hono.client.username=messaging@<tenant_id> --hono.client.password=<password> --tenant.id=<tenant_id> --device.id=<deviceId> --export.ip=localhost:8086

