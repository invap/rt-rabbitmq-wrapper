# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from enum import Enum, auto
from abc import abstractmethod

from rt_rabbitmq_wrapper.exchange_types.verdict.verdict import Verdict, NoVerdictSubtypeError


class ProcessVerdict(Verdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, verdict) -> None:
        super().__init__(timestamp, verdict)

    @staticmethod
    def verdict_type():
        return "process_verdict"

    @staticmethod
    def verdict_subtype():
        raise NoVerdictSubtypeError

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
