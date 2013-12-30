#!/usr/bin/env python

from distutils.core import setup

# From http://stackoverflow.com/a/16624700/1290530
from pip.req import parse_requirementsi
install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(name='snapchat-fs',
      version='0.1',
      description='Turns Snapchat into a datastore that can manage and store your files',
      author='Chad Brubaker, Alex Clemmer, Michael Rosenberg',
      packages=['snapchat_core', 'snapchat_fs'],
      scripts=['sfs'],
      install_requires=reqs
     )
