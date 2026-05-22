# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from abc import abstractmethod
from rt_rabbitmq_wrapper.exchange_types.event.event import NoEventSubtypeError
from rt_rabbitmq_wrapper.exchange_types.event.process_event import ProcessEvent


class TaskEvent(ProcessEvent):
    def __init__(self, name, time) -> None:
        super().__init__(time)
        self._name = name

    def name(self):
        return self._name

    @staticmethod
    def event_subtype():
        raise NoEventSubtypeError

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
