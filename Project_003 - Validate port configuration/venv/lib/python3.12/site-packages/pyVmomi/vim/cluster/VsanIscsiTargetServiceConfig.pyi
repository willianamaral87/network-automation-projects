# Copyright (c) 2006-2025 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.

# ******* WARNING - AUTO GENERATED CODE - DO NOT EDIT *******

from typing import Optional

from pyVmomi.vmodl import DynamicData

from pyVmomi.vim.cluster import VsanIscsiTargetServiceDefaultConfigSpec

from pyVmomi.vim.vsan import VipConfigSpec

class VsanIscsiTargetServiceConfig(DynamicData):
   defaultConfig: Optional[VsanIscsiTargetServiceDefaultConfigSpec] = None
   enabled: Optional[bool] = None
   vipConfigs: list[VipConfigSpec] = []
