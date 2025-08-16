# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from enum import Enum, auto


class Verdict:
    def __init__(self, timestamp, verdict):
        self._timestamp = timestamp
        self._verdict = verdict

    def timestamp(self):
        return self._timestamp

    def verdict(self):
        return self._verdict


class ProcessVerdict(Verdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, verdict) -> None:
        super().__init__(timestamp, verdict)


class TaskStartedVerdict(ProcessVerdict):
    def __init__(self, timestamp, name, verdict) -> None:
        super().__init__(timestamp, verdict)
        self._name = name

    def task_name(self):
        return self._name


class TaskFinishedVerdict(ProcessVerdict):
    def __init__(self, timestamp, name, verdict) -> None:
        super().__init__(timestamp, verdict)
        self._name = name

    def task_name(self):
        return self._name


class CheckpointReachedVerdict(ProcessVerdict):
    def __init__(self, timestamp, name, verdict) -> None:
        super().__init__(timestamp, verdict)
        self._name = name

    def checkpoint_name(self):
        return self._name


class AnalysisVerdict(Verdict):
    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, verdict)
        self._property_name = property_name
        self._spec_build_time = spec_build_time
        self._analysis_time = analysis_time

    def property_name(self):
        return self._property_name

    def spec_build_time(self):
        return self._spec_build_time

    def analysis_time(self):
        return self._analysis_time


class PyVerdict(AnalysisVerdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property_name, verdict, spec_build_time, analysis_time)


class SymPyVerdict(AnalysisVerdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property_name, verdict, spec_build_time, analysis_time)


class SMT2Verdict(AnalysisVerdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()
        MIGHT_FAIL = auto()

    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property_name, verdict, spec_build_time, analysis_time)
