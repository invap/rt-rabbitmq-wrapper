# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

import logging
# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)

from rt_rabbitmq_wrapper.exchange_types.verdict.verdict import (
    ProcessVerdict,
    TaskStartedVerdict,
    TaskFinishedVerdict,
    CheckpointReachedVerdict,
    AnalysisVerdict,
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
    # Converts a verdict to a dictionary
    @staticmethod
    def to_csv(verdict):
        if isinstance(verdict, ProcessVerdict):
            return VerdictCSVCoDec._process_verdict_to_csv(verdict)
        elif isinstance(verdict, AnalysisVerdict):
            return VerdictCSVCoDec._analysis_verdict_to_csv(verdict)
        else:
            logger.error(f"Invalid verdict type.")
            raise InvalidVerdict()

    @staticmethod
    def _process_verdict_to_csv(verdict):
        if isinstance(verdict, TaskStartedVerdict):
            return VerdictCSVCoDec._task_started_verdict_to_dict(verdict)
        elif isinstance(verdict, TaskFinishedVerdict):
            return VerdictCSVCoDec._task_finished_verdict_to_dict(verdict)
        elif isinstance(verdict, CheckpointReachedVerdict):
            return VerdictCSVCoDec._checkpoint_reached_verdict_to_dict(verdict)
        else:
            logger.error(f"Invalid process verdict type.")
            raise InvalidVerdict()

    @staticmethod
    def _task_started_verdict_to_dict(verdict):
        return "task_started"+","+str(verdict.timestamp())+","+verdict.task_name()+","+verdict.verdict().name

    @staticmethod
    def _task_finished_verdict_to_dict(verdict):
        return "task_finished"+","+str(verdict.timestamp())+","+verdict.task_name()+","+verdict.verdict().name

    @staticmethod
    def _checkpoint_reached_verdict_to_dict(verdict):
        return "checkpoint_reached"+","+str(verdict.timestamp())+","+verdict.checkpoint_name()+","+verdict.verdict().name

    @staticmethod
    def _analysis_verdict_to_csv(verdict):
        if isinstance(verdict, SMT2Verdict):
            return VerdictCSVCoDec._smt2verdict_to_csv(verdict)
        elif isinstance(verdict, PyVerdict):
            return VerdictCSVCoDec._pyverdict_to_csv(verdict)
        elif isinstance(verdict, SymPyVerdict):
            return VerdictCSVCoDec._sympyverdict_to_csv(verdict)
        else:
            logger.error(f"Invalid verdict type.")
            raise InvalidVerdict()

    @staticmethod
    def _smt2verdict_to_csv(verdict):
        return "smt2"+","+str(verdict.timestamp())+","+verdict.property_name()+","+verdict.verdict().name+","+verdict.spec_build_time()+","+verdict.analysis_time()

    @staticmethod
    def _pyverdict_to_csv(verdict):
        return "py"+","+str(verdict.timestamp())+","+verdict.property_name()+","+verdict.verdict().name+","+verdict.spec_build_time()+","+verdict.analysis_time()

    @staticmethod
    def _sympyverdict_to_csv(verdict):
        return "sympy"+","+str(verdict.timestamp())+","+verdict.property_name()+","+verdict.verdict().name+","+verdict.spec_build_time()+","+verdict.analysis_time()

    @staticmethod
    def from_csv(string):
        event_type = VerdictCSVCoDec._verdict_type_from_csv(string)
        match event_type:
            case "task_started":
                return VerdictCSVCoDec._task_started_verdict_from_csv(string)
            case "task_finished":
                return VerdictCSVCoDec._task_finished_from_csv(string)
            case "checkpoint_reached":
                return VerdictCSVCoDec._checkpoint_reached_verdict_from_csv(string)
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
        split_string = string.split(",", 1)
        if len(split_string) < 2:
            logger.error(f"Invalid verdict csv.")
            raise InvalidVerdictCSV()
        else:
            return split_string[0]

    @staticmethod
    def _task_started_verdict_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid verdict csv.")
            raise InvalidVerdictCSV()
        else:
            try:
                verdict = TaskStartedVerdict(int(split_string[1]), split_string[2], ProcessVerdict.VERDICT[split_string[3]])
            except (IndexError, KeyError):
                logger.error(f"Invalid verdict csv.")
                raise InvalidVerdictCSV()
            else:
                return verdict

    @staticmethod
    def _task_finished_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid verdict csv.")
            raise InvalidVerdictCSV()
        else:
            try:
                verdict = TaskFinishedVerdict(int(split_string[1]), split_string[2], ProcessVerdict.VERDICT[split_string[3]])
            except (IndexError, KeyError):
                logger.error(f"Invalid verdict csv.")
                raise InvalidVerdictCSV()
            else:
                return verdict

    @staticmethod
    def _checkpoint_reached_verdict_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid verdict csv.")
            raise InvalidVerdictCSV()
        else:
            try:
                verdict = CheckpointReachedVerdict(int(split_string[1]), split_string[2], ProcessVerdict.VERDICT[split_string[3]])
            except (IndexError, KeyError):
                logger.error(f"Invalid verdict csv.")
                raise InvalidVerdictCSV()
            else:
                return verdict

    @staticmethod
    def _smt2verdict_from_csv(string):
        split_string = string.split(",", 5)
        if len(split_string) < 6:
            logger.error(f"Invalid verdict csv.")
            raise InvalidVerdictCSV()
        else:
            try:
                verdict = SMT2Verdict(int(split_string[1]), split_string[2], SMT2Verdict.VERDICT[split_string[3]], split_string[4], split_string[5])
            except (IndexError, KeyError):
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
                verdict = PyVerdict(int(split_string[1]), split_string[2], PyVerdict.VERDICT[split_string[3]], split_string[4], split_string[5])
            except (IndexError, KeyError):
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
                verdict = SymPyVerdict(int(split_string[1]), split_string[2], SymPyVerdict.VERDICT[split_string[3]], split_string[4], split_string[5])
            except (IndexError, KeyError):
                logger.error(f"Invalid verdict csv.")
                raise InvalidVerdictCSV()
            else:
                return verdict
