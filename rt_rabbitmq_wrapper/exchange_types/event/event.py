# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from abc import ABC, abstractmethod


class Event(ABC):
    def __init__(self, timestamp):
        self._timestamp = timestamp

    def timestamp(self):
        return self._timestamp

    @staticmethod
    def event_type():
        raise NotImplementedError

    @staticmethod
    def event_subtype():
        raise NotImplementedError

    @abstractmethod
    def process_with(self, monitor):
        raise NotImplementedError
