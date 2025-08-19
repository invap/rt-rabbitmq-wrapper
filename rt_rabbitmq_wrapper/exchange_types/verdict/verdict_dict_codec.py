# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

import logging
# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)

from rt_rabbitmq_wrapper.exchange_types.verdict.verdict_codec_errors import (
    VerdictTypeError,
    VerdictDictError
)
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


# Raises: VerdictTypeError()
class VerdictDictCoDec:
    # Converts a verdict to a dictionary
    @staticmethod
    def to_dict(verdict):
        if isinstance(verdict, ProcessVerdict):
            return VerdictDictCoDec._process_verdict_to_dict(verdict)
        elif isinstance(verdict, AnalysisVerdict):
            return VerdictDictCoDec._analysis_verdict_to_dict(verdict)
        else:
            logger.error(f"Invalid verdict type.")
            raise VerdictTypeError()

    # Converts a process verdict to a dictionary
    @staticmethod
    def _process_verdict_to_dict(verdict):
        if isinstance(verdict, TaskStartedVerdict):
            return VerdictDictCoDec._task_started_verdict_to_dict(verdict)
        elif isinstance(verdict, TaskFinishedVerdict):
            return VerdictDictCoDec._task_finished_verdict_to_dict(verdict)
        elif isinstance(verdict, CheckpointReachedVerdict):
            return VerdictDictCoDec._checkpoint_reached_verdict_to_dict(verdict)
        else:
            logger.error(f"Invalid process verdict type.")
            raise VerdictTypeError()

    @staticmethod
    def _task_started_verdict_to_dict(verdict):
        return {
            "type": "task_started",
            "timestamp": verdict.timestamp,
            "task_name": verdict.task_name,
            "verdict": verdict.verdict.name
        }

    @staticmethod
    def _task_finished_verdict_to_dict(verdict):
        return {
            "type": "task_finished",
            "timestamp": verdict.timestamp,
            "task_name": verdict.task_name,
            "verdict": verdict.verdict.name
        }

    @staticmethod
    def _checkpoint_reached_verdict_to_dict(verdict):
        return {
            "type": "checkpoint_reached",
            "timestamp": verdict.timestamp,
            "checkpoint_name": verdict.checkpoint_name,
            "verdict": verdict.verdict.name
        }

    # Converts an analysis verdict to a dictionary
    @staticmethod
    def _analysis_verdict_to_dict(verdict):
        if isinstance(verdict, SMT2Verdict):
            return VerdictDictCoDec._smt2verdict_to_dict(verdict)
        elif isinstance(verdict, PyVerdict):
            return VerdictDictCoDec._pyverdict_to_dict(verdict)
        elif isinstance(verdict, SymPyVerdict):
            return VerdictDictCoDec._sympyverdict_to_dict(verdict)
        else:
            logger.error(f"Invalid analysis verdict type.")
            raise VerdictTypeError()

    @staticmethod
    def _smt2verdict_to_dict(verdict):
        return {
            "type": "smt2",
            "timestamp": verdict.timestamp,
            "property_name": verdict.property_name,
            "verdict": verdict.verdict.name,
            "spec_build_time": verdict.spec_build_time,
            "analysis_time": verdict.analysis_time
        }

    @staticmethod
    def _pyverdict_to_dict(verdict):
        return {
            "type": "py",
            "timestamp": verdict.timestamp,
            "property_name": verdict.property_name,
            "verdict": verdict.verdict.name,
            "spec_build_time": verdict.spec_build_time,
            "analysis_time": verdict.analysis_time
        }

    @staticmethod
    def _sympyverdict_to_dict(verdict):
        return {
            "type": "sympy",
            "timestamp": verdict.timestamp,
            "property_name": verdict.property_name,
            "verdict": verdict.verdict.name,
            "spec_build_time": verdict.spec_build_time,
            "analysis_time": verdict.analysis_time
        }

    @staticmethod
    def from_dict(verdict_dict):
        try:
            match verdict_dict["type"]:
                case "task_started":
                    try:
                        return TaskStartedVerdict(
                            verdict_dict["timestamp"],
                            verdict_dict["task_name"],
                            ProcessVerdict.VERDICT[verdict_dict["verdict"]]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "task_finished":
                    try:
                        return TaskFinishedVerdict(
                            verdict_dict["timestamp"],
                            verdict_dict["task_name"],
                            ProcessVerdict.VERDICT[verdict_dict["verdict"]]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "checkpoint_reached":
                    try:
                        return CheckpointReachedVerdict(
                            verdict_dict["timestamp"],
                            verdict_dict["checkpoint_name"],
                            ProcessVerdict.VERDICT[verdict_dict["verdict"]]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "smt2":
                    try:
                        return SMT2Verdict(
                            verdict_dict["timestamp"],
                            verdict_dict["property_name"],
                            SMT2Verdict.VERDICT[verdict_dict["verdict"]],
                            verdict_dict["spec_build_time"],
                            verdict_dict["analysis_time"]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "py":
                    try:
                        return PyVerdict(
                            verdict_dict["timestamp"],
                            verdict_dict["property_name"],
                            PyVerdict.VERDICT[verdict_dict["verdict"]],
                            verdict_dict["spec_build_time"],
                            verdict_dict["analysis_time"]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
                case "sympy":
                    try:
                        return SymPyVerdict(
                            verdict_dict["timestamp"],
                            verdict_dict["property_name"],
                            SymPyVerdict.VERDICT[verdict_dict["verdict"]],
                            verdict_dict["spec_build_time"],
                            verdict_dict["analysis_time"]
                        )
                    except KeyError:
                        logger.error(f"Invalid verdict.")
                        raise VerdictDictError()
        except KeyError:
            logger.error(f"Invalid dictionary key set for building a verdict.")
            raise VerdictDictError()
