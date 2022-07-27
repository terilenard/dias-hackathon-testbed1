Firewall and Intrusion Detection System
=======================================

The Firewall (FW) and IDS (Intrusion Detection System) basically function on the same **Rule Processing Engine** (denoted in the following as RPE). Depending on how the rules are written in it's associated **rule file**, the RPE will function as a Stateful Firewall, analyzing sequences of CAN frames based on their identifier field, or as a Intrusion Detection System, by performing a byte-level inspection in the CAN frame data field.

This means, that the FW/IDS is mainly composed in a single process capable of acting in a specific way, depending on it's configuration.

Installation
----------------


Configuration
-----------------

Firewall/IDS
------------------

A configuration file is used by the Firewall/IDS process to store a set of parameters. The configuration file named *diasfw.cfg*, and can be found in */etc/diasfw/*. It contains the followings:

* *ruleFile* : the location of the XML file, containing the Firewall/IDS set of rules.
* *secureLog* : boolean value under the form of a string. If *"true"* the process will leverage the Secure Logging process to generate signed logs. Else, if it is *"false"* the logs are saved  (file logging, syslog?).
* *canPipe*: path to a named piped used to communicate with a helper process that reads and preprocesses CAN frames. 
* *tpmPipe*: path to a named pipe used to communicate with the Secure Logging process.

Pycan
-----------

The pycan configuration file *config.py* is located in */etc/diasfw/*. The parameters of interest are the following:

* *PIPE_PATH* : path to a named piped used to communicate with the Firewall/IDS
* *CAN_CHANNEL_REC* : the process will listen for CAN interface on this interface. If a combination of physical interface and virutal interface was chosen than the value for this parameter should be the physical interface (e.g., CAN0). 
* *CAN_CHANNEL_SEND* : the process will forward the incomming frames to this interface. For the current demo those frames will not be used. If a combination of physical interface and virutal interface was chosen than the value for this parameter should be the virtual interface (e.g., VCAN0), else if a combination of two  virutal interfaces was chosen than the value for this parameter should be VCAN1.
* *LOGFILE* : the location of the pycan log file.
