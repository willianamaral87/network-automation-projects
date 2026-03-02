# Copyright (c) 2006-2025 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.

# ******* WARNING - AUTO GENERATED CODE - DO NOT EDIT *******

from typing import Optional

from pyVmomi.VmomiSupport import ManagedObject

from pyVmomi.vim import Task
from pyVmomi.vim import TaskDescription
from pyVmomi.vim import TaskFilterSpec
from pyVmomi.vim import TaskHistoryCollector
from pyVmomi.vim import TaskInfo
from pyVmomi.vim import TaskInfoFilterSpec

from pyVmomi.vmodl import DynamicData

class TaskManager(ManagedObject):
   class TaskViewSpec(DynamicData):
      pass

   class ViewByStartId(TaskViewSpec):
      count: int
      startId: str

   @property
   def recentTask(self) -> list[Task]: ...
   @property
   def description(self) -> TaskDescription: ...
   @property
   def maxCollector(self) -> int: ...

   def CreateCollector(self, filter: TaskFilterSpec) -> TaskHistoryCollector: ...
   def CreateCollectorWithInfoFilter(self, filter: TaskFilterSpec, infoFilter: Optional[TaskInfoFilterSpec]) -> TaskHistoryCollector: ...
   def CreateTask(self, obj: ManagedObject, taskTypeId: str, initiatedBy: Optional[str], cancelable: bool, parentTaskKey: Optional[str], activationId: Optional[str]) -> TaskInfo: ...
   def ReadNextTasksByViewSpec(self, viewSpec: TaskViewSpec, filterSpec: TaskFilterSpec, infoFilterSpec: Optional[TaskInfoFilterSpec]) -> list[TaskInfo]: ...
