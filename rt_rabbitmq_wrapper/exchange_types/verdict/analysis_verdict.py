# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from abc import ABC, abstractmethod
from enum import Enum

from rt_rabbitmq_wrapper.exchange_types.verdict.verdict import NoVerdictSubtypeError, Verdict


class AnalysisVerdict(Verdict):
    @property
    @abstractmethod
    class VERDICT(Enum):
        pass
    
    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, verdict)
        self._property_name = property_name
        self._spec_build_time = spec_build_time
        self._analysis_time = analysis_time

    @property
    def property_name(self):
        return self._property_name

    @property
    def spec_build_time(self):
        return self._spec_build_time

    @property
    def analysis_time(self):
        return self._analysis_time

    @staticmethod
    def verdict_type():
        return "analysis_verdict"

    @staticmethod
    def verdict_subtype():
        raise NoVerdictSubtypeError

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass