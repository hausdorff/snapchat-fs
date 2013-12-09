#!/usr/bin/env python

"""
snaps.py provides Python objects that represent Snaps of various forms --
received, sent, and so on. Methods in these classes encapsulate actions
that are useful to perform on snaps.
"""

from Crypto.Cipher import AES

__author__ = "Alex Clemmer, Chad Brubaker"
__copyright__ = "Copyright 2013, Alex Clemmer and Chad Brubaker"
__credits__ = ["Alex Clemmer", "Chad Brubaker"]

__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Alex Clemmer"
__email__ = "clemmer.alexander@gmail.com"
__status__ = "Prototype"


class Caption():
    def __init__(self, text, location, orientation):
        self.text = text
        self.location = location
        self.orientation = orientation

    @staticmethod
    def from_json(snap):
        if not snap.has_key('cap_text'):
            return None
        return Caption(snap['cap_text'],
                       snap['cap_pos'],
                       snap['cap_ori'])
class Snap():
    encryption_key = "M02cnQ51Ji97vwT4"

    class Type():
        """
        The media type of Snap
        """
        IMAGE = 0
        VIDEO = 1
        VIDEO_NO_AUDIO = 2
        FRIEND_REQ = 3
        FRIEND_REQ_IMAGE = 4
        FRIEND_REQ_VIDEO = 5
        FRIEND_REQ_VIDEO_NO_AUDIO = 6

    class State():
        """
        The state of the Snap.

        Snaps that are viewed are (claimed to be) deleted from the server
        """
        SENT = 0
        DELIVERED = 1
        VIEWED = 2
        SCREENSHOT = 3


    @property
    def viewable(self):
        return self.state == Snap.State.DELIVERED and self.type != Snap.Type.FRIEND_REQ

    def download(self, when = None, skip_decrypt = False):
        """
        Download a snap from the server.
        """
        if not self.viewable:
            raise Exception("Snap not viewable, cannot download")

        if when is None:
            when = str(int(time.time() * 100))

        params = {'id' : self.id, 'timestamp' : when, 'username' : self.connection.username}
        result = self.connection.send_req("/bq/blob", params, when).content
        if skip_decrypt:
            return result
        # test if result is unencrypted
        if result[:3] == '\x00\x00\x00' and results[5:12] == '\x66\x74\x79\x70\x33\x67\x70\x35':
            return result
        elif result[:3] == '\xFF\xD8\xFF':
            return result

        # otherwise encrypted, decrypt it.
        crypt = AES.new(self.encryption_key, AES.MODE_ECB)
        result = bytes(crypt.decrypt(result))
        # remove padding
        result = result[:-ord(result[-1])]
        return result

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

class SentSnap(Snap):

    def __init__(self, connection, id, client_id, recipient, type, state, timestamp, send_timestamp,\
                 view_time = 0, screenshots = 0, caption = None):
        self.connection = connection
        self.id = id
        self.client_id = client_id
        self.recipient = recipient
        self.user = recipient
        self.type = type
        self.state = state
        self.timestamp = timestamp
        self.send_timestamp = timestamp
        self.screenshots = screenshots
        self.caption = caption

    @staticmethod
    def from_json(conn, snap):
        return SentSnap(conn,
                        snap['id'],
                        snap['c_id'],
                        snap['rp'],
                        snap['m'],
                        snap['st'],
                        snap['ts'],
                        snap['sts'],
                        snap.get('t',0),
                        snap.get('ss', 0),
                        Caption.from_json(snap))
    @property
    def viewable(self):
        return False

class ReceivedSnap(Snap):

    def __init__(self, connection, id, sender, type, state, timestamp, send_timestamp,\
            view_time = 0, screenshots = 0, caption = None):
        self.connection = connection
        self.id = id
        self.sender = sender
        self.user = sender
        self.type = type
        self.state = state
        self.timestamp = timestamp
        self.send_timestamp = timestamp
        self.screenshots = screenshots
        self.caption = caption

    @staticmethod
    def from_json(conn, snap):
        return ReceivedSnap(conn,
                        snap['id'],
                        snap['sn'],
                        snap['m'],
                        snap['st'],
                        snap['ts'],
                        snap['sts'],
                        snap.get('t',0),
                        snap.get('ss', 0),
                        Caption.from_json(snap))
