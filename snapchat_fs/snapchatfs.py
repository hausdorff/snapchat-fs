#!/usr/bin/env python

"""
snapchatfs.py provides a clean CLI for uploading, storing, managing, and
downloading arbitrary data files from Snapchat.
"""

import hashlib, os
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

def download_all_sfs(username, password, target_dir):
    # get all downloadable files tracked by Snapchat FS
    files = all_downloadable_sfs_files(username, password)

    filenames_downloaded = set()
    for filename, content_hash, received_id, snap in files:
        try:
            data = snap.download()
            if filename not in filenames_downloaded:
                print("Downloading snap %s" % filename)
                path = os.path.join(target_dir, filename)
            else:
                print("Non-unique filename: downloading snap %s as %s" %
                      (filename, filename + "-" + content_hash))
                path = os.path.join(target_dir
                                    , filename + "-" + content_hash)

            filenames_downloaded.add(filename)
            with open(os.path.join(target_dir, filename+content_hash)
                      , 'w') as w:
                w.write(data)

        except Exception as e:
            print("Failed to download %s: %s" % (filename, e))
            raise

def all_downloadable_sfs_files(username, password):
    ss = SfsSession(username, password)
    ss.login()

    # get list of downloadable ids
    downloadable_snaps = ss.get_snaps(lambda snap: snap.viewable)
    downloadable_snaps_dict = {snap.id: snap
                              for snap in downloadable_snaps}

    # get list of snaps sent
    snaps_sent = ss.get_snaps(lambda snap: isinstance(snap, SentSnap)
                              and SfsSession.is_sfs_id(snap.client_id))

    # for deduping -- a file is a duplicate if its content and its name
    # are the same
    filenames_seen_so_far = set()
    content_seen_so_far = set()

    # grab all "unique" files stored in Snapchat FS
    sfs_files = []
    for snap in snaps_sent:
        filename, content_hash = ss.parse_sfs_id(snap.client_id)
        received_id = sent_id_to_received_id(snap.id)

        if (filename in filenames_seen_so_far) \
           and (content_hash in content_seen_so_far):
            continue
        elif received_id in downloadable_snaps_dict:
            filenames_seen_so_far.add(filename)
            content_seen_so_far.add(content_hash)
            downloadable_snap = downloadable_snaps_dict[received_id]
            sfs_files.append((filename, content_hash, received_id
                              , downloadable_snap))

    return sfs_files

def list_all_downloadable_sfs_files(username, password):
    files = all_downloadable_sfs_files(username, password)

    print '\t'.join([bold('Filename'), bold('Content hash')])
    for filename, content_hash, received_id, snap in files:
        print '%s\t%s...%s' % (filename, content_hash[:17]
                               , content_hash[-3:])
