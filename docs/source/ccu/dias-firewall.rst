6. Firewall and Intrusion Detection System
==========================================

The Firewall (FW) and IDS (Intrusion Detection System) basically function on the same **Rule Processing Engine** (denoted in the following as RPE). Depending on how the rules are written in it's associated **rule file**, the RPE will function as a Stateful Firewall, analyzing sequences of CAN frames based on their identifier field, or as a Intrusion Detection System, by performing a byte-level inspection in the CAN frame data field.

This means, that the FW/IDS is mainly composed in a single process capable of acting in a specific way, depending on it's configuration.

6.1. Requirements
-----------------

* CAN interface and vcan0 configured


6.2. Installation
------------------

Navigate to *toolchain/scripts* and execute the install script:

.. code::

    ./firewall.sh
    

6.3. Configuration
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


6.4. Rule language
==================

The set of rules contained in the rule file are described using a Extensible Markup Language (XML) based language. 
A pattern is defined as an *action rule*, which ultimately is applied on every data frame. An *action rule* can be linked together with a sequence of *action rules* creating a *state-chain*. This describes actions that must be taken on a sequence of frames, thus providing contextual detection capabilities. Subsequently, each *action rule* provides the ability to generate a hierarchical expression, allowing definitions for deep packet inspection rules. This step leverages boolean operators, such as *AND* and *OR*, used to link together different expressions.
 
6.4.1 Terms and keywords
------------------------

1. **Rule file** : an XML file containing the definitions for the *rules*, *actions* as well as the way the rules are chained togheter creating the *rule-chains* and *state-chains*.
2. **Rule** : a pattern searched within an incoming CAN frame. Each rule is bound to an *action*, which in term triggers an event if a pattern is found.   
3. **Action** : the operation that must take place as a consequence to a specific event. An action can have one of the four values: PERMIT, DROP, PERMIT-LOG and DROP-LOG.
 a. *PERMIT* : the incomming frame should be allowed to pass.
 b. *DROP* : the frame shound not be further forwarded.
 c. *PERMIT-LOG* :  the incomming frame should be allowed to pass, additionaly the event should be logged by the Secure Logging unit.
 d. *DROP-LOG* : the frame shound not be further forwarded, additionaly the event should be logged by the Secure Logging unit.


.. code-block:: XML

      <!-- FIREWALL TEST RULE for CID: 124 (hex) -->
      <rule cid="292" id="test_frame_2" action="PERMIT">
      </rule>

      The above rule (FIREWALL) will PERMIT all frames with the CID 292 (124 in hex).

      <!-- IDS TEST RULE for CID: 123 (hex) -->
      <rule cid="291" id="test_frame" actrion="DROP">
        <payload>
          <expression>
            <operator type="AND">
              <byte index="0" value="1"/>
              <byte index="1" value-range="1..170"/>
            </operator>
          </expression>
        </payload>
      </rule>

    The above rule (IDS) will DROP all frames with the CID 291 (123 in hex) if the first byte from the payload
    has the value 1 and the second byte has a value in the range [1,170].

6.4.2. State chains
-------------------

In the **state chains** the rules are chained together in sequences of rules, allowing the SFW/IDS to make decisions on a current frame, based on the past received traffic.
 
.. code-block:: XML

  <state-chains>
    <chain id="state-chain-1">
      <rule id="1-permit" action="PERMIT"/>
      <rule id="2-permit" action="PERMIT"/>
      <rule id="3-drop" action="DROP"/>
    </chain>
  </state-chains>

 In the above example a state chain is defined, containing 3 chained rules.

6.5. Frequency Processing
-------------------------
TODO
