#!/usr/bin/env python

"""
util.py provides a set of nice utility functions that support the snapchat_fs pkg
"""

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

def green(text):
    return '\033[1;32m%s\033[0m' % text

def red(text):
    return '\033[1;31m%s\033[0m' % text

