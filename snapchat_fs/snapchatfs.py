#!/usr/bin/env python

"""
snapchatfs.py provides a clean CLI for uploading, storing, managing, and
downloading arbitrary data files from Snapchat.
"""

import hashlib
from snapchat_core import SnapchatSession

__author__ = "Alex Clemmer, Chad Brubaker"
__copyright__ = "Copyright 2013, Alex Clemmer and Chad Brubaker"
__credits__ = ["Alex Clemmer", "Chad Brubaker"]

__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Alex Clemmer"
__email__ = "clemmer.alexander@gmail.com"
__status__ = "Prototype"


def generate_sfs_id(filename):
	"""
	Produces an ID for a file stored in Snapchat FS. ID consists of a prefix, the
	filename, and a unique identifier based on file data.
	@filename Name of the file as it exists on the filesystem.
	@file_data The data inside the file.
	"""
        with open(filename) as f:
            file_data = f.read()
	sha = hashlib.sha256()
	sha.update(file_data)
	content_id = sha.hexdigest()
	return "snapchatfs-%s-%s" % (filename, content_id)


if __name__ == '__main__':
    # TODO: FILL IN YOUR CREDENTIALS HERE.
    #ss = SnapchatSession('', '')
    ss.login()
    filename = 'file.txt'
    sfs_id = generate_sfs_id(filename)
    ss.upload_image(filename, sfs_id)
    ss.send_image_to('abecedarius', sfs_id)

