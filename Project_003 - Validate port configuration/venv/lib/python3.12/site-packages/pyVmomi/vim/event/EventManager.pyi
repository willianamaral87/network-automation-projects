# Copyright (c) 2006-2025 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.

# ******* WARNING - AUTO GENERATED CODE - DO NOT EDIT *******

from typing import NoReturn
from typing import Optional

from pyVmomi.VmomiSupport import ManagedObject

from pyVmomi.vim import ManagedEntity
from pyVmomi.vim import TaskInfo

from pyVmomi.vmodl import DynamicData

from pyVmomi.vim.event import Event
from pyVmomi.vim.event import EventDescription
from pyVmomi.vim.event import EventFilterSpec
from pyVmomi.vim.event import EventHistoryCollector

class EventManager(ManagedObject):
   class EventViewSpec(DynamicData):
      pass

   class ViewByStartId(EventViewSpec):
      startEventId: int
      isForward: bool

   @property
   def description(self) -> EventDescription: ...
   @property
   def latestEvent(self) -> Optional[Event]: ...
   @property
   def maxCollector(self) -> int: ...

   def RetrieveArgumentDescription(self, eventTypeId: str) -> list[EventDescription.EventArgDesc]: ...
   def CreateCollector(self, filter: EventFilterSpec) -> EventHistoryCollector: ...
   def LogUserEvent(self, entity: ManagedEntity, msg: str) -> NoReturn: ...
   def QueryEvent(self, filter: EventFilterSpec, eventViewSpec: Optional[EventViewSpec]) -> list[Event]: ...
   def PostEvent(self, eventToPost: Event, taskInfo: Optional[TaskInfo]) -> NoReturn: ...
