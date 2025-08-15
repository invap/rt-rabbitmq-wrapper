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
    InvalidVerdictCSV
)


# Raises: InvalidEvent()
class VerdictCSVCoDec:
    # Converts an event to a dictionary
    @staticmethod
    def to_csv(verdict):
        if isinstance(verdict, SMT2Verdict):
            return VerdictCSVCoDec._smt2verdict_to_csv(verdict)
        elif isinstance(verdict, PyVerdict):
            return VerdictCSVCoDec._pyverdict_to_csv(verdict)
        elif isinstance(verdict, SymPyVerdict):
            return VerdictCSVCoDec._sympyverdict_to_csv(verdict)
        else:
            logger.error(f"Invalid Event type.")
            raise InvalidVerdict()

    @staticmethod
    def _smt2verdict_to_csv(verdict):
        return ("smt2"+","+str(verdict.timestamp())+","+verdict.property()+","+verdict.verdict()+","+verdict.spec_build_time()+","+verdict.analysis_time())

    @staticmethod
    def _pyverdict_to_csv(verdict):
        return ("py"+","+str(verdict.timestamp())+","+verdict.property()+","+verdict.verdict()+","+verdict.spec_build_time()+","+verdict.analysis_time())

    @staticmethod
    def _sympyverdict_to_csv(verdict):
        return ("sympy"+","+str(verdict.timestamp())+","+verdict.property()+","+verdict.verdict()+","+verdict.spec_build_time()+","+verdict.analysis_time())

    @staticmethod
    def from_csv(string):
        event_type = VerdictCSVCoDec._verdict_type_from_csv(string)
        match event_type:
            case "smt2":
                return VerdictCSVCoDec._smt2verdict_from_csv(string)
            case "py":
                return VerdictCSVCoDec._pyverdict_from_csv(string)
            case "sympy":
                return VerdictCSVCoDec._sympyverdict_from_csv(string)
            case _:
                logger.error(f"Invalid event csv for Verdict.")
                raise InvalidVerdictCSV()

    @staticmethod
    def _verdict_type_from_csv(string):
        split_string = string.split(",", 2)
        if len(split_string) < 3:
            logger.error(f"Invalid verdict csv.")
            raise InvalidVerdictCSV()
        else:
            return split_string[1]

    @staticmethod
    def _smt2verdict_from_csv(string):
        split_string = string.split(",", 5)
        if len(split_string) < 6:
            logger.error(f"Invalid verdict csv.")
            raise InvalidVerdictCSV()
        else:
            try:
                verdict = SMT2Verdict(split_string[1], split_string[2], split_string[3], split_string[4], split_string[5])
            except IndexError:
                logger.error(f"Invalid verdict csv.")
                raise InvalidVerdictCSV()
            else:
                return verdict

    @staticmethod
    def _pyverdict_from_csv(string):
        split_string = string.split(",", 5)
        if len(split_string) < 6:
            logger.error(f"Invalid verdict csv.")
            raise InvalidVerdictCSV()
        else:
            try:
                verdict = SMT2Verdict(split_string[1], split_string[2], split_string[3], split_string[4], split_string[5])
            except IndexError:
                logger.error(f"Invalid verdict csv.")
                raise InvalidVerdictCSV()
            else:
                return verdict

    @staticmethod
    def _sympyverdict_from_csv(string):
        split_string = string.split(",", 5)
        if len(split_string) < 6:
            logger.error(f"Invalid verdict csv.")
            raise InvalidVerdictCSV()
        else:
            try:
                verdict = SMT2Verdict(split_string[1], split_string[2], split_string[3], split_string[4], split_string[5])
            except IndexError:
                logger.error(f"Invalid verdict csv.")
                raise InvalidVerdictCSV()
            else:
                return verdict
