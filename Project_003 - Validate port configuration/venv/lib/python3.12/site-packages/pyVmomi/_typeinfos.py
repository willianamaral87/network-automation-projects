# Copyright (c) 2005-2025 Broadcom. All Rights Reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.


def load_typeinfos():
    try:
        from . import _typeinfo_core
    except ImportError:
        pass

    try:
        from . import _typeinfo_eam
    except ImportError:
        pass

    try:
        from . import _typeinfo_pbm
    except ImportError:
        pass

    try:
        from . import _typeinfo_query
    except ImportError:
        pass

    try:
        from . import _typeinfo_sms
    except ImportError:
        pass

    try:
        from . import _typeinfo_vim
    except ImportError:
        pass

    try:
        from . import _typeinfo_vslm
    except ImportError:
        pass

    from .VmomiSupport import SetFreezeDefinitions  # noqa: E402
    try:
        SetFreezeDefinitions(True)
        from . import _typeinfo_vsanhealth
    except ImportError:
        pass
    finally:
        SetFreezeDefinitions(False)
