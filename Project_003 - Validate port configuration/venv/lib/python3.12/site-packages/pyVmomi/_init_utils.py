# Copyright (c) 2025 Broadcom. All Rights Reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

from .five import pyMajor, pyMinor

if (pyMajor, pyMinor) < (3, 9):
    msg = "Python 3.9 or newer is required (found {0}.{1})".format(pyMajor, pyMinor)
    raise Exception(msg)
