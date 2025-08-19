# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from enum import Enum, auto
from abc import ABC, abstractmethod


class Verdict(ABC):
    def __init__(self, timestamp, verdict):
        self._timestamp = timestamp
        self._verdict = verdict

    @abstractmethod
    def __str__(self):
        pass

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def verdict(self):
        return self._verdict


class ProcessVerdict(Verdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, verdict) -> None:
        super().__init__(timestamp, verdict)

    @abstractmethod
    def __str__(self):
        pass


class TaskStartedVerdict(ProcessVerdict):
    def __init__(self, timestamp, name, verdict) -> None:
        super().__init__(timestamp, verdict)
        self._name = name

    @property
    def task_name(self):
        return self._name

    def __str__(self):
        return f"Event: task_started - Task name: {self.task_name} - Timestamp: {self.timestamp} - Verdict: {self.verdict}"


class TaskFinishedVerdict(ProcessVerdict):
    def __init__(self, timestamp, name, verdict) -> None:
        super().__init__(timestamp, verdict)
        self._name = name

    @property
    def task_name(self):
        return self._name

    def __str__(self):
        return f"Event: task_finished - Task name: {self.task_name} - Timestamp: {self.timestamp} - Verdict: {self.verdict}"


class CheckpointReachedVerdict(ProcessVerdict):
    def __init__(self, timestamp, name, verdict) -> None:
        super().__init__(timestamp, verdict)
        self._name = name

    @property
    def checkpoint_name(self):
        return self._name

    def __str__(self):
        return f"Event: checkpoint_reached - Checkpoint name: {self.checkpoint_name} - Timestamp: {self.timestamp} - Verdict: {self.verdict}"


class AnalysisVerdict(Verdict):
    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, verdict)
        self._property_name = property_name
        self._spec_build_time = spec_build_time
        self._analysis_time = analysis_time

    @abstractmethod
    def __str__(self):
        pass

    @property
    def property_name(self):
        return self._property_name

    @property
    def spec_build_time(self):
        return self._spec_build_time

    @property
    def analysis_time(self):
        return self._analysis_time


class PyVerdict(AnalysisVerdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property_name, verdict, spec_build_time, analysis_time)

    def __str__(self):
        return f"Analyzed property: {self.property_name} - Timestamp: {self.timestamp} - Spec. build time: {self.spec_build_time} - Analysis time: {self.analysis_time} - Verdict: {self.verdict}"


class SymPyVerdict(AnalysisVerdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property_name, verdict, spec_build_time, analysis_time)

    def __str__(self):
        return f"Analyzed property: {self.property_name} - Timestamp: {self.timestamp} - Spec. build time: {self.spec_build_time} - Analysis time: {self.analysis_time} - Verdict: {self.verdict}"


class SMT2Verdict(AnalysisVerdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()
        MIGHT_FAIL = auto()

    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property_name, verdict, spec_build_time, analysis_time)

    def __str__(self):
        return f"Analyzed property: {self.property_name} - Timestamp: {self.timestamp} - Spec. build time: {self.spec_build_time} - Analysis time: {self.analysis_time} - Verdict: {self.verdict}"
