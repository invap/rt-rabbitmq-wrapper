# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from abc import ABC, abstractmethod
from enum import Enum


class NoVerdictTypeError(Exception):
    def __init__(self):
        super().__init__()


class NoVerdictSubtypeError(Exception):
    def __init__(self):
        super().__init__()


class Verdict(ABC):
    @property
    @abstractmethod
    class VERDICT(Enum):
        pass

    def __init__(self, timestamp, verdict):
        self._timestamp = timestamp
        self._verdict = verdict

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def verdict(self):
        return self._verdict

    @staticmethod
    def verdict_type():
        raise NoVerdictTypeError

    @staticmethod
    def verdict_subtype():
        raise NoVerdictSubtypeError

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

