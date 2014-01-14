# -*- coding: utf-8 -*-
"""
    Sphinx configuration file for building em's documentation.
"""
from __future__ import unicode_literals

import re
import os
import sys


# add parent dir to PYTHONPATH for allowing import em's version
sys.path.append(os.path.abspath(os.pardir))
from em import __version__ as em_version


# project settings
project = 'em'
copyright = '2014, Igor Kalnitsky'
release = em_version
version = re.sub('[^0-9.]', '', release)

# sphinx settings
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

# html output settings
html_theme = 'default'
html_static_path = ['_static']
html_show_sourcelink = True
htmlhelp_basename = 'emdoc'
