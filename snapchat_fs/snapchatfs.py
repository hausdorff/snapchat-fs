#!/usr/bin/env python

"""
snapchatfs.py provides a clean CLI for uploading, storing, managing, and
downloading arbitrary data files from Snapchat.
"""

from __future__ import absolute_import
import hashlib, os
import snapchat_fs.util as util
from snapchat_core import *

__author__ = "Alex Clemmer, Chad Brubaker"
__copyright__ = "Copyright 2013, Alex Clemmer and Chad Brubaker"
__credits__ = ["Alex Clemmer", "Chad Brubaker"]

__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Alex Clemmer"
__email__ = "clemmer.alexander@gmail.com"
__status__ = "Prototype"


def sent_id_to_received_id(id):
    """
    Transforms a sent_id to a received_id.
    
    Sent IDs have an 's' at the end, while received IDs have an 'r' on the
    end. This method strips 's' off and replaces it with an 'r'.

    @id Id to transform.
    @return Transformed id.
    """
    return id[:-1] + 'r'

def download_all_sfs(session, target_dir):
    """
    Downloads all files managed by Snapchat FS, writing them to `target_dir`
    
    @session An SfsSession object that has been logged in.
    @target_dir Where to download the files to.
    """
    files = all_downloadable_sfs_files(session)
    download_from_sfs(target_dir, files)

def download_by_id(session, target_dir, snap_ids):
    """
    Downloads files managed by Snapchat FS with specified ids,
    writing them to `target_dir`
    
    @session An SfsSession object that has been logged in.
    @target_dir Where to download the files to.
    @snap_ids The ids of the snaps to download
    """
    def should_download_file(f):
        (_, _, _, snap) = f
        return snap.id in snap_ids

    # get all downloadable files tracked by Snapchat FS
    available_files = all_downloadable_sfs_files(session)
    files_to_download = filter(should_download_file, available_files)
    download_from_sfs(target_dir, files_to_download)

def download_from_sfs(target_dir, files):
    """
    Downloads snaps given a list of Snap objects, writing them to `target_dir`

    @target_dir Where to download the files to.
    @files The list of (filename, content_hash, recv_id, snap) tuples to download
    """

    # download each file in sequence; if we find two files with the same
    # name, we give the file a name that includes a hash of the contents
    filenames_downloaded = set()
    for filename, content_hash, received_id, snap in files:
        try:
            data = snap.download()
            if filename not in filenames_downloaded:
                print(util.green("Downloading snap ") + filename)
                path = os.path.join(target_dir, filename)
            else:
                print(util.green("Downloading snap ") + filename +
                      (util.red("but filename is not unique; ") +
                       ("downloading as: %s" %
                        (filename + "-" + content_hash))))
                path = os.path.join(target_dir
                                    , filename + "-" + content_hash)

            filenames_downloaded.add(filename)
            with open(os.path.join(target_dir, filename+content_hash)
                      , 'w') as w:
                w.write(data)

        except Exception as e:
            print("Failed to download %s: %s" % (filename, e))
            raise

def all_downloadable_sfs_files(session):
    """
    Gets all files managed in Snapchat FS for a specific user; returns
    them as a list of Snap objects, whose IDs can be used to download
    all or some of the files from Snapchat's DB.
    
    @session An SfsSession object that has been logged in.
    @return List of Snap objects representing the files.
    """

    # get list of downloadable ids
    downloadable_snaps = session.get_snaps(lambda snap: snap.viewable)
    downloadable_snaps_dict = {snap.id: snap
                              for snap in downloadable_snaps}

    # get list of snaps sent
    snaps_sent = session.get_snaps(lambda snap: isinstance(snap, SentSnap)
                                   and SfsSession.is_sfs_id(snap.client_id))

    # for deduping -- a file is a duplicate if its content and its name
    # are the same
    filenames_seen_so_far = set()
    content_seen_so_far = set()

    # grab all "unique" files stored in Snapchat FS
    sfs_files = []
    for snap in snaps_sent:
        filename, content_hash = session.parse_sfs_id(snap.client_id)
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

def list_all_downloadable_sfs_files(session):
    """
    Produces a list of Snap objects representing all downloadable files
    managed by Snapchat FS for a particular user.
    
    @session An SfsSession object that has been logged in.
    @return List of Snap objects representing all downloadable files in SFS.
    """
    files = all_downloadable_sfs_files(session)

    print '\t'.join([util.bold('Filename'), util.bold('Content hash'), util.bold('Snap ID')])
    for filename, content_hash, received_id, snap in files:
        print '%s\t%s...%s\t%s' % (filename, content_hash[:17]
                               , content_hash[-3:], snap.id)

def upload_sfs_file(session, filename):
    """
    Uploads a file to Snapchat FS.

    @session An SfsSession object that has been logged in.
    @filename Path of the file to upload.
    """
    with open(filename) as f:
        data = f.read()

    basename = os.path.basename(filename)
    print util.green('Uploading file ') + (basename)
    sfs_id = session.generate_sfs_id(basename, data)
    session.upload_image(data, sfs_id)
    session.send_image_to(username, sfs_id)
