0. Bosch IoT Hub Setup
======================

The `Bosch IoT Hub <https://bosch-iot-suite.com/service/bosch-iot-device-management/>`_ cloud service is used to receive MQTT data published by the mqtt client from the In-Vehicle clients, that must be processed by cloud services. This steps described in this documentation are necesary to configure both, some In-Vehicle services (e.g., log publisher, cloudfeeder) and cloud ones (e.g., Hono consumers). The document shows you how to and where to create a account, how to access the Bosch IoT Hub Management API, and how to create virtual devices so services can connect successfully to the hub.

0.1 Account Creations
---------------------

1. Go to the Bosch IoT Hub `main page <https://bosch-iot-suite.com/>`_.

2. Click the *User* icon top right, and then *Sign-in* to create a new account.

3. Once the account is create you can go further.


0.2 Subscription
----------------

1. After your account was created successfully and you are logging in go to the `Subscription page <https://accounts.bosch-iot-suite.com/subscriptions/>`_ .

2. Click the *New Subscription* button to create a service instance.

3. On the page you were redirected, select *Bosch IoT Device Management* service pack. This will create a 30 service instance that can be used in the testbed.

0.3 OAuth2 Client
-----------------

To use the Mangement API, a client with credentials must be generated trough the portal.

1. On the main `Subscription page <https://accounts.bosch-iot-suite.com/subscriptions/>`_ go to the the *OAuth2 Clients* tab.

2. Click the *New OAuth2 Client* button to create new client credential and secret.

3. After the client credetials were created, you should be on the *OAuth2 Client Details* page. If not go back on the `OAuth2 Clients <https://accounts.bosch-iot-suite.com/oauth2-clients/>`_ tab, and click the *Details* option in the client table.

4. On the *OAuth2 Client Details* page click the *Use* button to obtain the *access token* you need to use for the Mangement API.

5. Save this access token, or keep it open since you need it to authenticate in the Management API page.

0.4 Mangement API
-----------------

Before moving forward, you will need some credentials from your subscription:

1. On the main `Subscription page <https://accounts.bosch-iot-suite.com/subscriptions/>`_ click the *Show credentials* button near your subscription instance.

2. From the json displayed, please save the *tenant_id*.

0.4.1 Authorize
--------------------

Go to the main page of the `Bosch IoT Hub Management API <https://apidocs.bosch-iot-suite.com/index.html?urls.primaryName=Bosch%20IoT%20Hub%20-%20Management%20API>`_. Before creating a device and its credentials, so you can send data to cloud, you need to authorized yourself.

1. Click the *Authorize* button.

2. Please use the first option *bearerAuth  (http, Bearer)*. In the *Value* text field, paste the *access token* you obtained from the *OAuth2 Client Details* page.

3. Lastly, click *Authorize* and the *Close*.

0.4.2 Create a device
---------------------

To create/register a device, you need to know your *tenant_id*, as mentioned in Section 0.4, and to be *Authorized* on the  `Bosch IoT Hub Management API <https://apidocs.bosch-iot-suite.com/index.html?urls.primaryName=Bosch%20IoT%20Hub%20-%20Management%20API>`_.

1. In the *device* section, select the *POST* - *register a device* option

2. Click the *Try it out* option to enable it.

3. Paste your *tenant_id* in the tenant-id text field.

4. Edit the request body:

.. code-block:: json

  {
    "device-id": "my_device",
    "enabled": true
  }

5. Click execute. If everything went allright, a 201 code was returned.

0.4.3 Create device credentials
-------------------------------

To generate credentials for a registered device, you need the *tenant_id*, the *device-id* of the device you created, and to be *Authorized* on the page.

1. Go to the *credentials* - *Manage credentials* section.

2. Click the *Add new credentials for a device.* *POST* option.

3. Click the *Try it out* option to enable it.

4. Paste the *tenant_id* in the proper text field.

5. Edit the request body:

.. code-block:: json

  {
    "device-id": "my_device",
    "type": "hashed-password",
    "auth-id": "my_device",
    "enabled": true,
    "secrets": [
      {
        "password": "my_device_password"
      }
    ]
  }
