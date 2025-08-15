# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

import logging
# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)

from rt_rabbitmq_wrapper.exchange_types.event.event_codec_errors import (
    InvalidEvent,
    InvalidEventCSV
)
from rt_rabbitmq_wrapper.exchange_types.event.timed_event import TimedEvent
from rt_rabbitmq_wrapper.exchange_types.event.state_event import StateEvent
from rt_rabbitmq_wrapper.exchange_types.event.component_event import ComponentEvent
from rt_rabbitmq_wrapper.exchange_types.event.process_event import ProcessEvent
from rt_rabbitmq_wrapper.exchange_types.event.clock_start_event import ClockStartEvent
from rt_rabbitmq_wrapper.exchange_types.event.clock_pause_event import ClockPauseEvent
from rt_rabbitmq_wrapper.exchange_types.event.clock_resume_event import ClockResumeEvent
from rt_rabbitmq_wrapper.exchange_types.event.clock_reset_event import ClockResetEvent
from rt_rabbitmq_wrapper.exchange_types.event.variable_value_assigned_event import VariableValueAssignedEvent
from rt_rabbitmq_wrapper.exchange_types.event.task_started_event import TaskStartedEvent
from rt_rabbitmq_wrapper.exchange_types.event.task_finished_event import TaskFinishedEvent
from rt_rabbitmq_wrapper.exchange_types.event.checkpoint_reached_event import CheckpointReachedEvent


# Raises: InvalidEvent()
class EventCSVCoDec:
    # Converts an event to a dictionary
    @staticmethod
    def to_csv(event):
        if isinstance(event, TimedEvent):
            return EventCSVCoDec._timed_event_to_csv(event)
        elif isinstance(event, StateEvent):
            return EventCSVCoDec._state_event_to_csv(event)
        elif isinstance(event, ProcessEvent):
            return EventCSVCoDec._process_event_to_csv(event)
        elif isinstance(event, ComponentEvent):
            return EventCSVCoDec._component_event_to_csv(event)
        else:
            logger.error(f"Invalid Event type.")
            raise InvalidEvent()

    # Converts a time event to a dictionary
    @staticmethod
    def _timed_event_to_csv(event):
        if isinstance(event, ClockPauseEvent):
            return EventCSVCoDec._clock_pause_event_to_csv(event)
        elif isinstance(event, ClockResetEvent):
            return EventCSVCoDec._clock_reset_event_to_csv(event)
        elif isinstance(event, ClockResumeEvent):
            return EventCSVCoDec._clock_resume_event_to_csv(event)
        elif isinstance(event, ClockStartEvent):
            return EventCSVCoDec._clock_start_event_to_csv(event)
        else:
            logger.error(f"Invalid TimeEvent subtype.")
            raise InvalidEvent()

    @staticmethod
    def _clock_pause_event_to_csv(event):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.clock_name()

    @staticmethod
    def _clock_reset_event_to_csv(event):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.clock_name()

    @staticmethod
    def _clock_resume_event_to_csv(event):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.clock_name()

    @staticmethod
    def _clock_start_event_to_csv(event):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.clock_name()

    # Converts a state event to a dictionary
    @staticmethod
    def _state_event_to_csv(event):
        if isinstance(event, VariableValueAssignedEvent):
            return EventCSVCoDec._variable_value_assigned_event_to_csv(event)
        else:
            logger.error(f"Invalid TimeEvent subtype.")
            raise InvalidEvent()

    @staticmethod
    def _variable_value_assigned_event_to_csv(event):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.variable_name() + "," + event.variable_value()

    # Converts a process event to a dictionary
    @staticmethod
    def _process_event_to_csv(event):
        if isinstance(event, TaskStartedEvent):
            return EventCSVCoDec._task_started_event_to_csv(event)
        elif isinstance(event, TaskFinishedEvent):
            return EventCSVCoDec._task_finished_event_to_csv(event)
        elif isinstance(event, CheckpointReachedEvent):
            return EventCSVCoDec._checkpoint_reached_event_to_csv(event)
        else:
            logger.error(f"Invalid TimeEvent subtype.")
            raise InvalidEvent()

    @staticmethod
    def _task_started_event_to_csv(event):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.name()

    @staticmethod
    def _task_finished_event_to_csv(event):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.name()

    @staticmethod
    def _checkpoint_reached_event_to_csv(event):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.name()

    # Converts a component event to a dictionary
    @staticmethod
    def _component_event_to_csv(event):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.component_name() + "," + event.data()

    # Converts a string to an event
    @staticmethod
    def from_csv(string):
        event_type = EventCSVCoDec._event_type_from_csv(string)
        match event_type:
            case "timed_event":
                return EventCSVCoDec._timed_event_from_csv(string)
            case "state_event":
                return EventCSVCoDec._state_event_from_csv(string)
            case "process_event":
                return EventCSVCoDec._process_event_from_csv(string)
            case "component_event":
                return EventCSVCoDec._component_event_from_csv(string)
            case "invalid":
                logger.error(f"Invalid event csv for Event.")
                raise InvalidEventCSV()
            case _:
                logger.error(f"Invalid event csv for Event.")
                raise InvalidEventCSV()

    # Converts a string to a timed event
    @staticmethod
    def _timed_event_from_csv(string):
        timed_event_type = EventCSVCoDec._timed_event_type_from_csv(string)
        match timed_event_type:
            case "clock_start":
                return EventCSVCoDec._clock_start_event_from_csv(string)
            case "clock_pause":
                return EventCSVCoDec._clock_pause_event_from_csv(string)
            case "clock_resume":
                return EventCSVCoDec._clock_resume_event_frm_csv(string)
            case "clock_reset":
                return EventCSVCoDec._clock_reset_event_from_csv(string)
            case _:
                raise InvalidEventCSV()

    @staticmethod
    def _timed_event_type_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[2]

    @staticmethod
    def _clock_start_event_from_csv(string):
        return ClockStartEvent(
            EventCSVCoDec._clock_name_from_csv(string),
            EventCSVCoDec._event_timestamp_from_csv(string),
        )

    @staticmethod
    def _clock_pause_event_from_csv(string):
        return ClockPauseEvent(
            EventCSVCoDec._clock_name_from_csv(string),
            EventCSVCoDec._event_timestamp_from_csv(string),
        )

    @staticmethod
    def _clock_resume_event_frm_csv(string):
        return ClockResumeEvent(
            EventCSVCoDec._clock_name_from_csv(string),
            EventCSVCoDec._event_timestamp_from_csv(string),
        )

    @staticmethod
    def _clock_reset_event_from_csv(string):
        return ClockResetEvent(
            EventCSVCoDec._clock_name_from_csv(string),
            EventCSVCoDec._event_timestamp_from_csv(string),
        )

    @staticmethod
    def _clock_name_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[3]

    # Converts a string to a state event
    @staticmethod
    def _state_event_from_csv(string):
        state_event_type = EventCSVCoDec._state_event_type_from_csv(string)
        match state_event_type:
            case "variable_value_assigned":
                return EventCSVCoDec._variable_value_assignment_event_from_csv(string)
            case _:
                logger.error(f"Invalid event csv for StateEvent.")
                raise InvalidEventCSV()

    @staticmethod
    def _state_event_type_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[2]

    @staticmethod
    def _variable_value_assignment_event_from_csv(string):
        return VariableValueAssignedEvent(
            EventCSVCoDec._variable_name_from_csv(string),
            EventCSVCoDec._variable_value_from_csv(string),
            EventCSVCoDec._event_timestamp_from_csv(string),
        )

    @staticmethod
    def _variable_name_from_csv(string):
        split_string = string.split(",", 4)
        if len(split_string) < 5:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[3]

    @staticmethod
    def _variable_value_from_csv(string):
        split_string = string.split(",", 4)
        if len(split_string) < 5:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[4]

    @staticmethod
    def _process_event_from_csv(string):
        process_event_type = EventCSVCoDec._process_event_type_from_csv(string)
        match process_event_type:
            case "task_started":
                return EventCSVCoDec._task_started_event_from_csv(string)
            case "task_finished":
                return EventCSVCoDec._task_finished_event_from_csv(string)
            case "checkpoint_reached":
                return EventCSVCoDec._checkpoint_reached_event_from_csv(string)
            case _:
                logger.error(f"Invalid event csv.")
                raise InvalidEventCSV()

    @staticmethod
    def _process_event_type_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[2]

    @staticmethod
    def _task_started_event_from_csv(string):
        return TaskStartedEvent(
            EventCSVCoDec._task_name_from_csv(string),
            EventCSVCoDec._event_timestamp_from_csv(string)
        )

    @staticmethod
    def _task_finished_event_from_csv(string):
        return TaskFinishedEvent(
            EventCSVCoDec._task_name_from_csv(string),
            EventCSVCoDec._event_timestamp_from_csv(string)
        )

    @staticmethod
    def _checkpoint_reached_event_from_csv(string):
        return CheckpointReachedEvent(
            EventCSVCoDec._checkpoint_name_from_csv(string),
            EventCSVCoDec._event_timestamp_from_csv(string),
        )

    @staticmethod
    def _task_name_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[3]

    @staticmethod
    def _checkpoint_name_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[3]

    # Converts a string to a component event
    @staticmethod
    def _component_event_from_csv(string):
        return ComponentEvent(
            EventCSVCoDec._component_name_from_csv(string),
            EventCSVCoDec._component_event_data_from_csv(string),
            EventCSVCoDec._event_timestamp_from_csv(string),
        )

    @staticmethod
    def _component_name_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[2]

    @staticmethod
    def _component_event_data_from_csv(string):
        split_string = string.split(",", 3)
        if len(split_string) < 4:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return bytes(split_string[3], "utf-8").decode("unicode_escape")

    @staticmethod
    def _event_type_from_csv(string):
        split_string = string.split(",", 2)
        if len(split_string) < 3:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return split_string[1]

    @staticmethod
    def _event_timestamp_from_csv(string):
        split_string = string.split(",", 2)
        if len(split_string) < 3:
            logger.error(f"Invalid event csv.")
            raise InvalidEventCSV()
        else:
            return int(split_string[0])
