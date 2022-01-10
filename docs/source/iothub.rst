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

0.4.1 Authentication
--------------------

0.4.2 Create a device
---------------------

0.4.3 Create device credentials
-------------------------------
