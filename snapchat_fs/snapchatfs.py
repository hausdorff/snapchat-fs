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


def bold(text):
    return '\033[1m%s\033[0m' % text

def sent_id_to_received_id(id):
    """
    Sent IDs have an 's' at the end, while received IDs have an 'r' on the
    end. This method strips 's' off and replaces it with an 'r'.
    """
    return id[:-1] + 'r'

def download_all_sfs(username, password):
    ss = SfsSession(username, password)
    ss.login()
    snaps = ss.get_snaps(lambda snap: isinstance(snap, SentSnap)
                         and SfsSession._is_sfs_id(snap.client_id))

    filenames_seen_so_far = set()
    content_seen_so_far = set()
    print '%s\t%s' % ('\033[1mFilename\033[0m'
                      , '\033[1mContent hash\033[0m')
    for snap in snaps:
        filename, content_hash = ss._parse_sfs_id(snap.client_id)

        if (filename in filenames_seen_so_far) \
           and (content_hash in content_seen_so_far):
            continue
        else:
            print '%s\t%s' % (filename, content_hash)
            filenames_seen_so_far.add(filename)
            content_seen_so_far.add(content_hash)

def all_downloadable_sfs_files(username, password):
    ss = SfsSession(username, password)
    ss.login()

    # get list of downloadable ids
    downloadable_snaps = ss.get_snaps(lambda snap: snap.viewable)
    downloadable_snaps_ids = set([snap.id for snap in downloadable_snaps])

    # get list of snaps sent
    snaps_sent = ss.get_snaps(lambda snap: isinstance(snap, SentSnap)
                              and SfsSession._is_sfs_id(snap.client_id))

    # for deduping -- a file is a duplicate if its content and its name
    # are the same
    filenames_seen_so_far = set()
    content_seen_so_far = set()

    # grab all "unique" files stored in Snapchat FS
    sfs_files = []
    for snap in snaps_sent:
        filename, content_hash = ss._parse_sfs_id(snap.client_id)
        received_id = sent_id_to_received_id(snap.id)

        if (filename in filenames_seen_so_far) \
           and (content_hash in content_seen_so_far):
            continue
        elif received_id in downloadable_snaps_ids:
            filenames_seen_so_far.add(filename)
            content_seen_so_far.add(content_hash)
            sfs_files.append((filename, content_hash, received_id, snap))

    return sfs_files

def list_all_downloadable_sfs_files(username, password):
    files = all_downloadable_sfs_files(username, password)

    print '\t'.join([bold('Filename'), bold('Content hash')])
    for filename, content_hash, received_id, snap in files:
        print '%s\t%s...%s' % (filename, content_hash[:17]
                               , content_hash[-3:])


if __name__ == '__main__':
    # TODO: FILL IN YOUR CREDENTIALS HERE.
    #ss = SnapchatSession('', '')
    ss.login()
    filename = 'file.txt'
    sfs_id = generate_sfs_id(filename)
    ss.upload_image(filename, sfs_id)
    ss.send_image_to('abecedarius', sfs_id)

