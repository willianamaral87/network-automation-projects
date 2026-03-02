# Copyright (c) 2025 Broadcom. All Rights Reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

import sys

pyMajor = sys.version_info[0]
pyMinor = sys.version_info[1]

PY3 = pyMajor >= 3

if PY3:
    from http.client import (HTTPConnection, HTTPSConnection)
    from urllib.parse import urlparse

    binary_type = bytes
    str_type = str
    text_type = str

    def iteritems(d):
        return d.items()

    def itervalues(d):
        return d.values()

else:
    from httplib import (HTTPConnection, HTTPSConnection)
    from urlparse import urlparse

    binary_type = str
    str_type = basestring
    text_type = unicode

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()

    import itertools  # noqa: E402

    map = itertools.imap
    range = xrange
    zip = itertools.izip
