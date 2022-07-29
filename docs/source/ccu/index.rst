5. Connectivity Control Unit Overview
=====================================

While the Electronic Control Unit (ECU) acts as a data sender, the Connectivity Control Unit (CCU) acts as a data receiver. Besides this role, in parallel the CCU has the responsability to distribute long term and short term cryptographic key in order to secure the communication between the two. Further more, the CCU act as the communication component in the Controller Area Network (CAN) network that handles communication with external services in the Cloud (Bosch IoT Insights).


5.1 Requirements
----------------

The following requirements must be meet before continuing configuring the ECU. The steps below are described in the Testbed dependencies page.


* Virtual CAN (vcan0) configured
* Mosquitto installed and configured with required usernames and passwords
* CAN interface connected and configured
* Compiled TPM2 dependencies
