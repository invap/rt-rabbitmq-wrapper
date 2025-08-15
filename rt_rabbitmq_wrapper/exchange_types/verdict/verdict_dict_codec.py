# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

import logging
# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)

from rt_rabbitmq_wrapper.exchange_types.verdict.verdict import (
    SMT2Verdict,
    PyVerdict,
    SymPyVerdict
)
from rt_rabbitmq_wrapper.exchange_types.verdict.verdict_codec_errors import (
    InvalidVerdict,
    InvalidVerdictDict
)


# Raises: InvalidEvent()
class VerdictDictCoDec:
    # Converts an event to a dictionary
    @staticmethod
    def to_dict(verdict):
        if isinstance(verdict, SMT2Verdict):
            return VerdictDictCoDec._smt2verdict_to_dict(verdict)
        elif isinstance(verdict, PyVerdict):
            return VerdictDictCoDec._pyverdict_to_dict(verdict)
        elif isinstance(verdict, SymPyVerdict):
            return VerdictDictCoDec._sympyverdict_to_dict(verdict)
        else:
            logger.error(f"Invalid Event type.")
            raise InvalidVerdict()

    @staticmethod
    def _smt2verdict_to_dict(verdict):
        return {
            "format": "smt2",
            "timestamp": verdict.timestamp(),
            "property": verdict.property(),
            "verdict": verdict.verdict(),
            "spec_build_time": verdict.spec_build_time(),
            "analysis_time": verdict.analysis_time()
        }

    @staticmethod
    def _pyverdict_to_dict(verdict):
        return {
            "format": "py",
            "timestamp": verdict.timestamp(),
            "property": verdict.property(),
            "verdict": verdict.verdict(),
            "spec_build_time": verdict.spec_build_time(),
            "analysis_time": verdict.analysis_time()
        }

    @staticmethod
    def _sympyverdict_to_dict(verdict):
        return {
            "format": "sympy",
            "timestamp": verdict.timestamp(),
            "property": verdict.property(),
            "verdict": verdict.verdict(),
            "spec_build_time": verdict.spec_build_time(),
            "analysis_time": verdict.analysis_time()
        }

    @staticmethod
    def from_dict(verdict_dict):
        try:
            match verdict_dict["format"]:
                case "smt2":
                    return SMT2Verdict(
                        verdict_dict["timestamp"],
                        verdict_dict["property"],
                        verdict_dict["verdict"],
                        verdict_dict["spec_build_time"],
                        verdict_dict["analysis_time"]
                    )
                case "py":
                    return PyVerdict(
                        verdict_dict["timestamp"],
                        verdict_dict["property"],
                        verdict_dict["verdict"],
                        verdict_dict["spec_build_time"],
                        verdict_dict["analysis_time"]
                    )
                case "sympy":
                    return SymPyVerdict(
                        verdict_dict["timestamp"],
                        verdict_dict["property"],
                        verdict_dict["verdict"],
                        verdict_dict["spec_build_time"],
                        verdict_dict["analysis_time"]
                    )
        except KeyError:
            logger.error(f"Invalid dictionary key set for building a Verdict.")
            raise InvalidVerdictDict()

