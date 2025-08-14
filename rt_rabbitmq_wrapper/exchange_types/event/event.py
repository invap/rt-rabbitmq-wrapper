# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from abc import abstractmethod


class EventError(Exception):
    def __init__(self):
        super().__init__()


class Event:
    def __init__(self, timestamp):
        self._timestamp = timestamp

    def timestamp(self):
        return self._timestamp

    @abstractmethod
    @staticmethod
    def event_type():
        raise NotImplementedError

    @abstractmethod
    @staticmethod
    def event_subtype():
        raise NotImplementedError

    @abstractmethod
    @staticmethod
    def decode_with(decoder, encoded_event):
        raise NotImplementedError

    @abstractmethod
    def process_with(self, monitor):
        raise NotImplementedError

    @abstractmethod
    def serialized(self):
        raise NotImplementedError
