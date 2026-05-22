# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

import logging

from rt_rabbitmq_wrapper.exchange_types.verdict.checkpoint_reached_verdict import CheckpointReachedVerdict
from rt_rabbitmq_wrapper.exchange_types.verdict.py_verdict import PyVerdict
from rt_rabbitmq_wrapper.exchange_types.verdict.smt2_verdict import SMT2Verdict
from rt_rabbitmq_wrapper.exchange_types.verdict.sympy_verdict import SymPyVerdict
from rt_rabbitmq_wrapper.exchange_types.verdict.task_finished_verdict import TaskFinishedVerdict
from rt_rabbitmq_wrapper.exchange_types.verdict.task_started_verdict import TaskStartedVerdict

# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)

from rt_rabbitmq_wrapper.exchange_types.verdict.analysis_verdict import AnalysisVerdict
from rt_rabbitmq_wrapper.exchange_types.verdict.process_verdict import ProcessVerdict
from rt_rabbitmq_wrapper.exchange_types.verdict.verdict_codec_errors import (
    VerdictTypeError,
    VerdictDictError
)


# Raises: VerdictTypeError()
class VerdictCSVCoDec:
    # Converts a verdict to a csv entry
    @staticmethod
    def to_csv(verdict):
        if isinstance(verdict, ProcessVerdict):
            return VerdictCSVCoDec._process_verdict_to_csv(verdict)
        elif isinstance(verdict, AnalysisVerdict):
            return VerdictCSVCoDec._analysis_verdict_to_csv(verdict)
        else:
            logger.error(f"Invalid verdict type.")
            raise VerdictTypeError()

    # Converts a process verdict to a csv entry
    @staticmethod
    def _process_verdict_to_csv(verdict):
        if isinstance(verdict, TaskStartedVerdict):
            return VerdictCSVCoDec._task_started_verdict_to_csv(verdict)
        elif isinstance(verdict, TaskFinishedVerdict):
            return VerdictCSVCoDec._task_finished_verdict_to_csv(verdict)
        elif isinstance(verdict, CheckpointReachedVerdict):
            return VerdictCSVCoDec._checkpoint_reached_verdict_to_csv(verdict)
        else:
            logger.error(f"Invalid process verdict type.")
            raise VerdictTypeError()

    @staticmethod
    def _task_started_verdict_to_csv(verdict):
        return f"{verdict.timestamp},task_started,{verdict.task_name},{verdict.verdict.name}"

    @staticmethod
    def _task_finished_verdict_to_csv(verdict):
        return f"{verdict.timestamp},task_finished,{verdict.task_name},{verdict.verdict.name}"

    @staticmethod
    def _checkpoint_reached_verdict_to_csv(verdict):
        return f"{verdict.timestamp},checkpoint_reached,{verdict.checkpoint_name},{verdict.verdict.name}"

    # Converts an analysis verdict to a csv entry
    @staticmethod
    def _analysis_verdict_to_csv(verdict):
        if isinstance(verdict, SMT2Verdict):
            return VerdictCSVCoDec._smt2verdict_to_csv(verdict)
        elif isinstance(verdict, PyVerdict):
            return VerdictCSVCoDec._pyverdict_to_csv(verdict)
        elif isinstance(verdict, SymPyVerdict):
            return VerdictCSVCoDec._sympyverdict_to_csv(verdict)
        else:
            logger.error(f"Invalid analysis verdict type.")
            raise VerdictTypeError()

    @staticmethod
    def _smt2verdict_to_csv(verdict):
        return f"{verdict.timestamp},smt2,{verdict.property_name},{verdict.verdict.name},{verdict.spec_build_time},{verdict.analysis_time}"

    @staticmethod
    def _pyverdict_to_csv(verdict):
        return f"{verdict.timestamp},py,{verdict.property_name},{verdict.verdict.name},{verdict.spec_build_time},{verdict.analysis_time}"

    @staticmethod
    def _sympyverdict_to_csv(verdict):
        return f"{verdict.timestamp},sympy,{verdict.property_name},{verdict.verdict.name},{verdict.spec_build_time},{verdict.analysis_time}"

    @staticmethod
    def from_csv(verdict_str):
        verdict_list = verdict_str.split(",")
        try:
            match verdict_list[0]:
                case "task_started":
                    try:
                        return TaskStartedVerdict(
                            verdict_list[1],
                            verdict_list[2],
                            ProcessVerdict.VERDICT[verdict_list[3]]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "task_finished":
                    try:
                        return TaskFinishedVerdict(
                            verdict_list[1],
                            verdict_list[2],
                            ProcessVerdict.VERDICT[verdict_list[3]]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "checkpoint_reached":
                    try:
                        return CheckpointReachedVerdict(
                            verdict_list[1],
                            verdict_list[2],
                            ProcessVerdict.VERDICT[verdict_list[3]]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "smt2":
                    try:
                        return SMT2Verdict(
                            verdict_list[1],
                            verdict_list[2],
                            SMT2Verdict.VERDICT[verdict_list[3]],
                            verdict_list[4],
                            verdict_list[5]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "py":
                    try:
                        return PyVerdict(
                            verdict_list[1],
                            verdict_list[2],
                            PyVerdict.VERDICT[verdict_list[3]],
                            verdict_list[4],
                            verdict_list[5]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "sympy":
                    try:
                        return SymPyVerdict(
                            verdict_list[1],
                            verdict_list[2],
                            SymPyVerdict.VERDICT[verdict_list[3]],
                            verdict_list[4],
                            verdict_list[5]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
        except KeyError:
            logger.error(f"Invalid dictionary key set for building a verdict.")
            raise VerdictDictError()
