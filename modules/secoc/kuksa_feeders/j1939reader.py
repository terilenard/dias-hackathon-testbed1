#!/usr/bin/python3

########################################################################
# Copyright (c) 2020 Robert Bosch GmbH
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0
########################################################################

"""
This script is to read CAN messages based on PGN - SAE J1939
Prior to using this script, j1939 and 
the relevant wheel-package should be installed first:
    $ pip install can-j1939
"""

import logging
import time
import re
import cantools
import j1939
import json
from threading import Timer
import secoc_verification
import client_mqtt

logging.getLogger('j1939').setLevel(logging.DEBUG)
logging.getLogger('can').setLevel(logging.DEBUG)

SIGNALSUSINGBUFFERING = re.compile("^DTC[0-9]+")

class J1939Reader(j1939.ControllerApplication):
    def __init__(self, cfg, rxqueue, mapper):
        # compose the name descriptor for the new ca
        name = j1939.Name(
            arbitrary_address_capable=0,
            industry_group=j1939.Name.IndustryGroup.Industrial,
            vehicle_system_instance=1,
            vehicle_system=1,
            function=1,
            function_instance=1,
            ecu_instance=1,
            manufacturer_code=666,
            identity_number=1234567
            )
        device_address_preferred = 128
        j1939.ControllerApplication.__init__(self, name, device_address_preferred)
        self.queue=rxqueue
        self.cfg=cfg
        self.db = cantools.database.load_file(cfg['dbcfile'])
        self.mapper=mapper
        self.canidwl = self.get_whitelist()
        self._timer = None
        self._error_count = 0
        self.mqtt_client = client_mqtt.MQTTClient("dbcfeeder", "dbcfeeder",
                                                  "127.0.0.1", 1883)
        self.mqtt_client.connect()

    def get_whitelist(self):
        print("Collecting signals, generating CAN ID whitelist")
        wl = []
        for entry in self.mapper.map():
            canid=self.get_canid_for_signal(entry[0])
            if canid != None and canid not in wl:
                wl.append(canid)
        return wl

    def get_canid_for_signal(self, sig_to_find):
        """
        Returns the CAN-ID of a given signalname as long as
        it is specified in the used .dbc file.
        """
        for msg in self.db.messages:
            for signal in msg.signals:
                if signal.name == sig_to_find:
                    id = msg.frame_id
                    print("Found signal {} in CAN frame id 0x{:02x}".format(signal._name, id))
                    return id
        print("Signal {} not found in DBC file".format(sig_to_find))
        return None

    def start_listening(self):
        """
        Connects to the Bus via socketcan and adds the CA (self) to
        an ECU. Starts the address claiming process at the end.
        """
        print("Open CAN device {}".format(self.cfg['port']))
        # create the ElectronicControlUnit (one ECU can hold multiple ControllerApplications)
        ecu = j1939.ElectronicControlUnit()
        # Connect to the CAN bus
        ecu.connect(bustype='socketcan', channel=self.cfg['port'])
        # add CA to the ECU
        ecu.add_ca(controller_application=self)
        #subscribe function on_message() to incoming messages
        self.subscribe(self.on_message)
        # starts the adress claiming procedure on the bus
        j1939.ControllerApplication.start(self)
        
    def get_raw_can(self, data):
        """
        Forms a hexadecimal string of a data byte array or data list.
        """
        hex_str = '0x'
        for i in range(len(data)):
            hex_str = hex_str + "{:02x}".format(data[i])
        return hex_str

    def identify_message(self, pgn, source):
        """
        Searchs for a message in the used .dbc file via its PGN
        """
        pgn_hex = hex(pgn)[2:] + "{:02x}".format(source)# only hex(pgn) and hex(source) without '0x' prefix
        for message in self.db.messages:
            message_hex = hex(message.frame_id)[-6:] # only hex(pgn) and hex(source) without '0x' prefix, priority and source address
            if pgn_hex == message_hex:
                return message
        return None

    def _start_timer(self):
        self._timer = Timer(5, self._on_timer)
        self._timer.start()

    def _on_timer(self):

        if self._error_count > 0:
            json_message = {}
            json_message["Message"] = "SecOC Authentication failed!"
            json_message["Count"] = self._error_count
            json_message["Timestamp"] = time.time()
            print("Publishing: error_count: {} json:{}".format(self._error_count, json.dumps(json_message)) )
            self.mqtt_client.publish(json.dumps(json_message))
            self._error_count = 0

        self._start_timer()

    def on_message(self, priority, pgn, source, timestamp, data):
        """
        Function callback for an incoming message.
        """
        message = self.identify_message(pgn, source)
        if message != None:
            signals = message._signals
            if 'SecOC' in message._name: # == "UpstreamNOxSecOC":
                if self.auth_message(data):
                    for signal in signals:
                        val = self.get_value_for_signal(signal, data)
                        self.put_signal_in_auth_queue(signal._name, val, 1)
                else:
                    self._error_count = self._error_count + 1
                    for signal in signals:
                        val = self.get_value_for_signal(signal, data)
                        self.put_signal_in_auth_queue(signal._name, val, 0)
            else:
                buffer = list()
                for signal in signals:
                    if len(data) * 8 >= signal.start + signal.length: # necessary for messages that are variable in length
                    # signal is available in data  
                        if SIGNALSUSINGBUFFERING.match(signal._name):
                            buffer.append(self.get_value_for_signal(signal, data))
                        else:
                            val = self.get_value_for_signal(signal, data)
                            self.put_signal_in_queue(signal._name, val)
                if len(buffer) != 0:
                    # as arrays are currently not supported by kuksa.val server use a string instead of []
                    # seperation of signals in string is: "{signal1}, {signal2}, {signal3}" e.g "1234, 1234, 'abc'" 
                    # -> seperator is ", "
                    buffer = str(buffer)[1:-1].replace("'","")
                    self.put_signal_in_queue(message.name + "_List", buffer)

    def put_signal_in_queue(self, name, val):
        """
        Puts the signal, its value and its target path according to the used .yml file into the queue of dbcfeeder.
        Checks if minimum update Time is elapsed.
        """
        if name in self.mapper:
            rxTime=time.time()
            if self.mapper.minUpdateTimeElapsed(name, rxTime):
                for target in self.mapper[name]['targets']:
                    tv=self.mapper.transform(name,target,val)
                    self.queue.put((name, tv, target))

    def put_signal_in_auth_queue(self, name, val, auth_status):
        """
        Same as put_signal_in_queue except for an additional look for auth_targets where the authentication status should be placed.
        """
        if name in self.mapper:
            rxTime=time.time()
            if self.mapper.minUpdateTimeElapsed(name, rxTime):
                for target in self.mapper[name]['targets']:
                    tv=self.mapper.transform(name,target,val)
                    self.queue.put((name, tv, target))
                for auth_target in self.mapper[name]['auth_status']:
                    self.queue.put((name, auth_status, auth_target))

                
    def auth_message(self, data):
        """
        Returns 1 if authenticated, 0 if not.
        """
        autosar = secoc_verification.SecocVerification(self.get_raw_can(data))
        if autosar.authentication_status():
            return 1
        else:
            return 0         

    def get_value_for_signal(self, signal, data):
        """
        Returns the real value of a signal. If minimum or maximum are exceeded it returns minimum value or maximum value respectively.
        """
        byte_order = signal._byte_order # 'little_endian' or 'big_endian'
        scale = signal._scale
        offset = signal._offset
        val = 0

        start_bit = signal._start
        num_of_bits = signal._length
        val = self.decode_signal(start_bit, num_of_bits, byte_order, scale, offset, data)

        if val < signal._minimum:
            val = signal._minimum
        elif val > signal._maximum:
            val = signal._maximum
        return val

    def decode_signal(self, start_bit, num_of_bits, byte_order, scale, offset, data):
        """
        Decode raw message data into one signals value.
        """
        binary_str = ''
        binstr = ''

        if byte_order == 'little_endian':
            for i in range(len(data)):
                dec = data[i]
                binstr = binstr + format(dec, '#010b')[2:][::-1]
            for i in range(0, num_of_bits):
                binary_str = binstr[start_bit + i] + binary_str
            
        else:
            start_bit = (start_bit - 2*(start_bit%8) + 7)
            for i in range(len(data)):
                dec = data[i]
                binstr = binstr + format(dec, '#010b')[2:]
            for i in range(0, num_of_bits):
                binary_str = binary_str + binstr[start_bit + i]

        binary_str = "0b" + binary_str
        raw_value = int(binary_str, base=2)
        val = offset + raw_value * scale
        return val

#Byte/Bit ordering
#
#Little endian:
#-> the most significant byte is the last one in the string
#-> bit 63 out of byte 7 has the highest value in the message
#+----------+----+----+----+----+----+----+----+----+
#| Byte/Bit | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0  |
#+----------+----+----+----+----+----+----+----+----+
#|        0 | 07 | 06 | 05 | 04 | 03 | 02 | 01 | 00 |
#|        1 | 15 | 14 | 13 | 12 | 11 | 10 | 09 | 08 |
#|        2 | 23 | 22 | 21 | 20 | 19 | 18 | 17 | 16 |
#|        3 | 31 | 30 | 29 | 28 | 27 | 26 | 25 | 24 |
#|        4 | 39 | 38 | 37 | 36 | 35 | 34 | 33 | 32 |
#|        5 | 47 | 46 | 45 | 44 | 43 | 42 | 41 | 40 |
#|        6 | 55 | 54 | 53 | 52 | 51 | 50 | 49 | 48 |
#|        7 | 63 | 62 | 61 | 60 | 59 | 58 | 57 | 56 |
#+----------+----+----+----+----+----+----+----+----+
#-> 07 06 05 04 03 02 01 00 | 15 14 13 12 11 10 09 08 | 23 22 21 20 19 18 17 16 | ...
#
#-> flip bit order in each byte so you get one string with adjacent bit levels
#-> 07 06 05 04 03 02 01 00 | 15 14 13 12 11 10 09 08 -> 00 01 02 03 04 05 06 07 | 08 09 10 11 12 13 14 15
#-> now you can extract the bits needed in one loop without considering byte borders or gaps 
#    (like in the first string the gap between the 8th element (00) and the 9th element (15))
#-> afterwards you just need to reverse the result string in order to position the most significant bit in first place to convert it into an integer afterwards
#
#Big endian:
#-> the most significant byte is the first one in the string
#-> bit 07 out of byte 0 has the highest value in the message
#+----------+----+----+----+----+----+----+----+----+
#| Byte/Bit | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0  |
#+----------+----+----+----+----+----+----+----+----+
#|        0 | 07 | 06 | 05 | 04 | 03 | 02 | 01 | 00 |
#|        1 | 15 | 14 | 13 | 12 | 11 | 10 | 09 | 08 |
#|        2 | 23 | 22 | 21 | 20 | 19 | 18 | 17 | 16 |
#|        3 | 31 | 30 | 29 | 28 | 27 | 26 | 25 | 24 |
#|        4 | 39 | 38 | 37 | 36 | 35 | 34 | 33 | 32 |
#|        5 | 47 | 46 | 45 | 44 | 43 | 42 | 41 | 40 |
#|        6 | 55 | 54 | 53 | 52 | 51 | 50 | 49 | 48 |
#|        7 | 63 | 62 | 61 | 60 | 59 | 58 | 57 | 56 |
#+----------+----+----+----+----+----+----+----+----+
#-> if you put the message in a string it would look like this:
#    - byte 0 | byte 1 | byte 2 | byte 3 | byte 4 | ... 
#-> since the first bit in every byte is the most significant bit, the string already has the correct order
#    (bit 40 has a higher value than bit 55 according to big endianess)
#
#Problem:
#-> for example most significant bit of a signal was 45, but bit 45 is not on position 45 in the bit string, because of the opposite counting direction
#    (bit 07 in above table would be bit 0 in the bit string)
#-> to find the start index of 45 in the bit string you need to do following steps:
#    1. find the least significant bit of the byte in which your start position is
#        - lsb = start_bit - (start-bit % 8)
#    2. find the most significant bit of the byte in which your start position is
#        - msb = lsb + 7
#    3. find the difference between your start position and the msb
#        - diff = msb - start_bit
#    4. your array index would be the difference added to the lsb
#        - index = lsb + diff
#    (5.) otherwise following equation will do exactly the same, just simplified:
#        - start_bit = (start_bit - 2*(start_bit%8) + 7)

