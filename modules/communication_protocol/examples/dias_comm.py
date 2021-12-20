'''
cladf/core/CladfCore

@author: Bela Genge
'''

import logging
import time
import datetime
from threading import Lock

from comm_core import (
    KEYMNGR_PUBSUB_ADDRESS, KEYMNGR_FRESHKEY_TOPIC)

from comm_core.communicator import Communicator
from comm_core.keymngr_pb2 import FreshDataAuthKey


class CommTest():

    def setup_communications(self):
        '''
        Method that sets-up the pub/sub communication channels.
        '''
        logging.info("Setting up ZeroMQ communications")

        self._communicator = Communicator(
            None,
            None,
            KEYMNGR_PUBSUB_ADDRESS,
            [],
            [Communicator.Subscription(
                KEYMNGR_PUBSUB_ADDRESS,
                [KEYMNGR_FRESHKEY_TOPIC], self._on_notification)])

        self._publish = self._communicator.publish

        return True


    def _on_notification(self, name, data):
        '''
        Method called when a notification is received.
        '''
        print("Notification: [{}, {}]".format(name, data))

        msg = FreshDataAuthKey()
        try:
            msg.ParseFromString(data)
            print("\tKey id: {}, Key: {}".format(msg.key_id, msg.key_value))

        except Exception as ex:
            print("Unexpected exception while processing notification: {}".format())


    def send_test_message(self):

        report = FreshDataAuthKey()
        report.key_id = 1234
        report.key_value = "BASE-64 ENCODED AND ENCRYPTED KEY"

        self._publish(KEYMNGR_FRESHKEY_TOPIC, report.SerializeToString())

comm = CommTest()
comm.setup_communications()
comm.send_test_message()
print("\nModule successfully started. Hit Ctrl+C to exit!\n\n")
