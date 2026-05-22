# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from abc import ABC, abstractmethod


class NoEventTypeError(Exception):
    def __init__(self):
        super().__init__()


class NoEventSubtypeError(Exception):
    def __init__(self):
        super().__init__()


class Event(ABC):
    def __init__(self, timestamp):
        self._timestamp = timestamp

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def event_type(self):
        raise NoEventTypeError

    @property
    def event_subtype(self):
        raise NoEventSubtypeError

    @abstractmethod
    def process_with(self, monitor):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
