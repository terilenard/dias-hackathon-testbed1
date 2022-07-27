Electronic Control Unit Overview
================================

The Electronic Control Unit (ECU) acts as a data sender to the Connectivity Control Unit (CCU). The ECU runs the following services:

* A instance of LTK-STK key exchange protocol. It receives via CAN securely Long-Term keys (LTKs) and Short-Term keys (STKs).
* MixCAN sender/slave, which authenticated CAN frames based on a set of preconfigured CAN ids. It leverages STKs for authentication tags computation.
* MQTT Broker, to enable communication between services and to allow easy future extensions and integration of other services. 

Requirements
------------
The following requirements must be meet before continuing configuring the ECU. The steps below are described in the *Testbed dependencies* page.

* Virtual CAN (vcan0) configured
* Mosquitto installed and configured with required usernames and passwords
* CAN interface connected and configured
* Compiled TPM2 dependencies
