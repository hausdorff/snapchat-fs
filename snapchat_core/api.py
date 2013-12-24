#!/usr/bin/env python

"""
api.py provides an opaque entry point to the Snapchat API. It backs all
the requests we will issue to the Snapchat service.
"""

import hashlib, requests, time
from Crypto.Cipher import AES
import constants
from friend import Friend
from snaps import Snap, SentSnap, ReceivedSnap

__author__ = "Alex Clemmer, Chad Brubaker"
__copyright__ = "Copyright 2013, Alex Clemmer and Chad Brubaker"
__credits__ = ["Alex Clemmer", "Chad Brubaker"]

__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Alex Clemmer"
__email__ = "clemmer.alexander@gmail.com"
__status__ = "Prototype"

# CONSTANTS; encodes strings used in the request headers by the Snapchat
# API. If they change, we only need to update these variables.
AUTH_TOKEN             = 'auth_token'
CAN_SEE_CUSTOM_STORIES = 'can_see_custom_stories'
CLIENT_ID              = 'id'
COUNTRY_CODE           = 'country_code'
DISPLAY                = 'display'
FRIENDS                = 'friends'
MEDIA_ID               = 'media_id'
NAME                   = 'name'
PASSWORD               = 'password'
RECIPIENT              = 'recipient'
REQ_TOKEN              = 'req_token'
SNAPS                  = 'snaps'
TIME                   = 'time'
TIMESTAMP              = 'timestamp'
TYPE                   = 'type'
USERNAME               = 'username'


class SnapchatSession():
    """
    Interacts with Snapchat API as a session. That is, you:
      (1) initialize the object with a username and password, which will
          result in a session being opened for you, and
      (2) issue different types of requests (send, upload, retry, etc.)
          using the corresponding methods.
    """

    def __init__(self, username, password):
        self.username = username  # string
        self.password = password  # string
        self.session_token = None # string
        self.snaps = None         # [Snap()]

    #
    # PUBLIC FACING API METHODS
    #
    def login(self):
        """
        Generates and executes the login request, populate session with
        state like number of friends, etc.
        """
        # wipe session state from previous sessions
        self.session_token = None

        # create parameters for current request, and issue request
        timestamp = SnapchatSession._generate_timestamp()
        req_params = {
              USERNAME  : self.username
            , PASSWORD  : self.password
            , TIMESTAMP : timestamp
            , REQ_TOKEN : SnapchatSession._generate_req_token(
                constants.LOGIN_TOKEN, timestamp)
        }

        result = SnapchatSession._post_or_fail(constants.LOGIN_RESOURCE
                                    , req_params).json()

        # make sure login was successful
        if result['logged'] == False:
            raise Exception("Login failed, invalid credentials")

        # update session state with login response information
        self.session_token = result[AUTH_TOKEN]
        self.login_data = result
        self._update_session_state(result)

    def upload_image(self, image_data, media_id):
        """
        Uploads an image to Snapchat.
        @image_data Image data to upload
        @media_id The ID to give the image we upload.
        """
        # generate request parameters
        encrypted_data = SnapchatSession._snapchat_basic_encrypt(
            image_data)
        timestamp = SnapchatSession._generate_timestamp()
        req_params = {
              USERNAME  : self.username
            , TIMESTAMP : timestamp
            , MEDIA_ID  : media_id
            , TYPE      : Snap.Type.IMAGE
            , REQ_TOKEN : SnapchatSession._generate_req_token(
                self.session_token, timestamp)
        }
        files = {'data' : ('file', encrypted_data)}

        # dispatch request
        result = SnapchatSession._post_or_fail(constants.UPLOAD_RESOURCE
                                               , req_params, files)

    def send_image_to(self, recipient, media_id, time = 10
                      , country_code = "US"):
        """
        Instructs Snapchat to send data to a user. Note that data must be
        uploaded to Snapchat before calling send_to.
        @recipient The username to send the snap to.
        @media_id The ID of the image to send.
        @time
        @country_code
        """
        #generate request parameters
        timestamp = SnapchatSession._generate_timestamp()
        params = {
              USERNAME     : self.username
            , TIMESTAMP    : timestamp
            , MEDIA_ID     : media_id
            , TYPE         : Snap.Type.IMAGE
            , COUNTRY_CODE : country_code
            , RECIPIENT    : recipient
            , TIME         : time
            , REQ_TOKEN    : SnapchatSession._generate_req_token(
                self.session_token, timestamp)
        }

        # dispatch request
        result = SnapchatSession._post_or_fail(constants.SEND_RESOURCE
                                               , params)

    def get_snaps(self, filter_func=lambda snap: True):
        """
        Returns array of Snaps sent to current user, represented as a list
        of Snap objects.
        @filter_func Filter function for snaps; takes a Snap object as
            input, returns `False` if we are to filter the Snap from our
            collection.
        """
        return filter(filter_func, self.snaps)

    def blob(self, client_id):
        timestamp = SnapchatSession._generate_timestamp()
        params = {
              USERNAME  : self.username
            , TIMESTAMP : timestamp
            , CLIENT_ID : client_id
            , REQ_TOKEN : SnapchatSession._generate_req_token(
                self.session_token, timestamp)
        }

        result = SnapchatSession._post_or_fail(constants.BLOB_RESOURCE
                                               , params).content
        
        if result[:3] == '\x00\x00\x00' \
           and results[5:12] == '\x66\x74\x79\x70\x33\x67\x70\x35':
            return result
        elif result[:3] == '\xFF\xD8\xFF':
            return result

        # otherwise encrypted, decrypt it.
        crypt = AES.new(constants.SECRET_KEY, AES.MODE_ECB)
        result = bytes(crypt.decrypt(result))
        # remove padding
        result = result[:-ord(result[-1])]
        return result


    #
    # PRIVATE UTILITY METHODS
    #
    @staticmethod
    def _snapchat_basic_encrypt(data):
        """
        Basic encryption technique used by Snapchat. It's ECB mode, which
        is a mode that should pretty much never be used, but we didn't
        pick it.
        @data The data to encrypt.
        """
        length = 16 - (len(data) % 16)
        data += chr(length) * length
        crypt = AES.new(constants.SECRET_KEY, AES.MODE_ECB)
        return crypt.encrypt(data)

    @staticmethod
    def _generate_req_token(server_token, timestamp):
        """
        Generates request token used by Snapchat's servers to "verify"
        that we don't have unauthorized access to their API.

        This consists of: generating two hashes, then zipping up the
        hashes from a pre-defined pattern.
        @server_token String representing session token given at login.
        @timestamp String representing timestamp of this request.
        """
        sha = hashlib.sha256()
        sha.update(constants.SALT + server_token)
        hash0 = sha.hexdigest()
        sha = hashlib.sha256()
        sha.update(timestamp + constants.SALT)
        hash1 = sha.hexdigest()

        output = [hash0[i] if constants.PATTERN[i] == '0' else hash1[i]
              for i in range(len(hash0))]
        
        return ''.join(output)

    @staticmethod
    def _generate_timestamp():
        """
        Generates string timestamp in the format used by Snapchat's API.
        """
        return str(int(time.time() * 100))

    @staticmethod
    def _post_or_fail(resource, request_params, files=None):
        """
        Issues a post request to the Snapchat API and fails if not 200 OK.
        @resource The resource to append to the URL root, e.g., /bq/login.
        @request_params Dictionary containing requests parameters, like
            username and password.
        @files A dict containing data from a file that we're adding to
            the POST request. Formatted like: {'data': ('file', data)}
        """
        uri = "%s%s" % (constants.ROOT_URL, resource)
        result = requests.post(uri, request_params, files = files)
        if result.status_code != 200:
            raise Exception("POST request failed with status code %d" %
                            (result.status_code))
        return result

    def _update_friends_list(self, json_update):
        """
        Updates the friends list using a dict representing the JSON object
        that was returned by the Snapchat API.
        @json_update Dictionary representing the JSON update returned by
            the Snapchat API.
        """
        friends = [Friend(friend[NAME], friend[DISPLAY], friend[TYPE]
                    , friend[CAN_SEE_CUSTOM_STORIES])
                   for friend in json_update[FRIENDS]]
        self.friends = friends

    def _update_session_state(self, json_update):
        """
        Updates the session's friends and snaps lists using a dict
        representing the JSON object that was returned by the Snapchat
        API.
        @json_update Dictionary representing the JSON update returned by
            the Snapchat API.
        """
        self._update_friends_list(json_update)
        self._update_snaps_list(json_update)

    def _update_snaps_list(self, json_update):
        """
        Updates the session's snaps list using a dict representing the
        JSON object that was returned by the Snapchat API.
        @json_update Dictionary representing the JSON update returned by
            the Snapchat API.
        """
        def _build_appropriate_snap_obj(snap):
            if snap.has_key('rp'):
                return SentSnap.from_json(self, snap)
            elif snap.has_key('sn'):
                return ReceivedSnap.from_json(self, snap)
            else:
                raise Exception("Unknown snap, no sender or receiver")            
        self.snaps = [_build_appropriate_snap_obj(snap)
                      for snap in json_update[SNAPS]]


class SfsSession(SnapchatSession):
    @staticmethod
    def generate_sfs_id(basename, file_data):
        """
        Produces an ID for a file stored in Snapchat FS. ID consists of a
        prefix, the
        filename, and a unique identifier based on file data.
        @filename Name of the file as it exists on the filesystem.
        @file_data The data inside the file.
        """
        sha = hashlib.sha256()
        sha.update(file_data)
        content_id = sha.hexdigest()
        return "snapchatfs-%s-%s" % (basename, content_id)

    @staticmethod
    def is_sfs_id(id):
        """
        Returns True if `id` is a valid Snapchat FS file identifier.
        @id The identifier to test.
        """
        return id.startswith('snapchatfs-')

    def parse_sfs_id(self, id):
        """
        Parses an identifier for a file in Snapchat FS. Returns the
        filename and a hash of
        the contents of the file.
        @id The Snapchat FS identifier to parse.
        """
        assert(SfsSession.is_sfs_id(id))
        # valid ids are of the form
        # """snapchat-[filename]-[hash of content][username]"""
        prefix = id[:11]                     # 'snapchat-'
        filename = id[11:-76]                # filename
        content_id = id[-75:-len(self.username)]  # hash of content
        return filename, content_id

