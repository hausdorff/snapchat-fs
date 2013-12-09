#!/usr/bin/env python

"""
snapchatfs.py provides a clean CLI for uploading, storing, managing, and
downloading arbitrary data files from Snapchat.
"""

import hashlib
from snapchat_core import *

__author__ = "Alex Clemmer, Chad Brubaker"
__copyright__ = "Copyright 2013, Alex Clemmer and Chad Brubaker"
__credits__ = ["Alex Clemmer", "Chad Brubaker"]

__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Alex Clemmer"
__email__ = "clemmer.alexander@gmail.com"
__status__ = "Prototype"


def list_all_sfs_files(username, password):
    ss = SfsSession(username, password)
    ss.login()

    filenames_seen_so_far = set()
    content_seen_so_far = set()
    print '%s\t%s' % ('\033[1mFilename\033[0m'
                      , '\033[1mContent hash\033[0m')
    for snap in ss.get_snaps(lambda snap: isinstance(snap, SentSnap)
                             and SfsSession._is_sfs_id(snap.client_id)):
        filename, content_hash = ss._parse_sfs_id(snap.client_id)

        if (filename in filenames_seen_so_far) \
           and (content_hash in content_seen_so_far):
            continue
        else:
            print '%s\t%s' % (filename, content_hash)
            filenames_seen_so_far.add(filename)
            content_seen_so_far.add(content_hash)


if __name__ == '__main__':
    # TODO: FILL IN YOUR CREDENTIALS HERE.
    #ss = SnapchatSession('', '')
    ss.login()
    filename = 'file.txt'
    sfs_id = generate_sfs_id(filename)
    ss.upload_image(filename, sfs_id)
    ss.send_image_to('abecedarius', sfs_id)

