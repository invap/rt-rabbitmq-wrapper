# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from enum import Enum, auto

from rt_rabbitmq_wrapper.exchange_types.verdict.analysis_verdict import AnalysisVerdict


class SymPyVerdict(AnalysisVerdict):
    class VERDICT(Enum):
        PASS = auto()
        FAIL = auto()

    def __init__(self, timestamp, property_name, verdict, spec_build_time, analysis_time) -> None:
        super().__init__(timestamp, property_name, verdict, spec_build_time, analysis_time)

    @staticmethod
    def verdict_subtype():
        return "sympy"

    def __str__(self):
        return f"(timestamp: {self.timestamp}) - sympy analysis(name: {self.property_name}, spec_build_time: {self.spec_build_time:3f}, analysis_time: {self.analysis_time:3f}, verdict: {self.verdict.name})"

    def __repr__(self):
        return f"(timestamp: {self.timestamp}) - sympy analysis(name: {self.property_name}, spec_build_time: {self.spec_build_time}, analysis_time: {self.analysis_time}, verdict: {self.verdict.name})"
