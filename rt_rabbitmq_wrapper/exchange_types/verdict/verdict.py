# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from enum import Enum, auto


class Verdict:
    def __init__(self, timestamp, property, verdict, spec_build_time, analysis_time):
        self._timestamp = timestamp
        self._property = property
        self._verdict = verdict
        self._spec_build_time = spec_build_time
        self._analysis_time = analysis_time

    def timestamp(self):
        return self._timestamp

    def property(self):
        return self._property

    def verdict(self):
        return self._verdict

    def spec_build_time(self):
        return self._spec_build_time

    def analysis_time(self):
        return self._analysis_time


class PyVerdict(Verdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, property, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property, verdict, spec_build_time, analysis_time)


class SymPyVerdict(Verdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, property, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property, verdict, spec_build_time, analysis_time)


class SMT2Verdict(Verdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()
        MIGHT_FAIL = auto()

    def __init__(self, timestamp, property, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property, verdict, spec_build_time, analysis_time)
