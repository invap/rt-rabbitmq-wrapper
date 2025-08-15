# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

import logging
# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)

from rt_rabbitmq_wrapper.exchange_types.event.event_codec_errors import InvalidEvent
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
            raise InvalidEvent(event)

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
            raise InvalidEvent(event)

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
            raise InvalidEvent(event)

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
            raise InvalidEvent(event)

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
        encoded_event = string.split(",", 3)
        # encoded_event is a list of strings [timestamp, event type, event, params depending on the specific event type and event]
        event_type = EventCSVCoDec._event_type_from_csv(encoded_event)
        match event_type:
            case "timed_event":
                return EventCSVCoDec._timed_event_from_csv(encoded_event)
            case "state_event":
                return EventCSVCoDec._state_event_from_csv(encoded_event)
            case "process_event":
                return EventCSVCoDec._process_event_from_csv(encoded_event)
            case "component_event":
                return EventCSVCoDec._component_event_from_csv(encoded_event)
            case "invalid":
                raise InvalidEvent(encoded_event)
            case _:
                # The execution should never match this case because the rt_reporter injects "invalid"
                # when the event reported is not af any of the above types.
                raise InvalidEvent(encoded_event)

    # Converts a string to a timed event
    @staticmethod
    def _timed_event_from_csv(encoded_event):
        timed_event_type = EventCSVCoDec._timed_event_type_from_csv(encoded_event)
        match timed_event_type:
            case "clock_start":
                return EventCSVCoDec._clock_start_event_from_csv(encoded_event)
            case "clock_pause":
                return EventCSVCoDec._clock_pause_event_from_csv(encoded_event)
            case "clock_resume":
                return EventCSVCoDec._clock_resume_event_frm_csv(encoded_event)
            case "clock_reset":
                return EventCSVCoDec._clock_reset_event_from_csv(encoded_event)
            case _:
                raise InvalidEvent(encoded_event)

    @staticmethod
    def _timed_event_type_from_csv(encoded_event):
        try:
            return encoded_event[2]
        except IndexError:
            raise InvalidEvent(encoded_event)

    @staticmethod
    def _clock_start_event_from_csv(encoded_event):
        return ClockStartEvent(
            EventCSVCoDec._clock_name_from_csv(encoded_event),
            EventCSVCoDec._event_timestamp_from_csv(encoded_event),
        )

    @staticmethod
    def _clock_pause_event_from_csv(encoded_event):
        return ClockPauseEvent(
            EventCSVCoDec._clock_name_from_csv(encoded_event),
            EventCSVCoDec._event_timestamp_from_csv(encoded_event),
        )

    @staticmethod
    def _clock_resume_event_frm_csv(encoded_event):
        return ClockResumeEvent(
            EventCSVCoDec._clock_name_from_csv(encoded_event),
            EventCSVCoDec._event_timestamp_from_csv(encoded_event),
        )

    @staticmethod
    def _clock_reset_event_from_csv(encoded_event):
        return ClockResetEvent(
            EventCSVCoDec._clock_name_from_csv(encoded_event),
            EventCSVCoDec._event_timestamp_from_csv(encoded_event),
        )

    @staticmethod
    def _clock_name_from_csv(encoded_event):
        encoded_parameters = EventCSVCoDec._event_parameters_from_csv(encoded_event)
        try:
            return encoded_parameters[1]
        except IndexError:
            raise InvalidEvent(encoded_event)

    # Converts a string to a state event
    @staticmethod
    def _state_event_from_csv(encoded_event):
        state_event_type = EventCSVCoDec._state_event_type_from_csv(encoded_event)
        match state_event_type:
            case "variable_value_assigned":
                return EventCSVCoDec._variable_value_assignment_event_from_csv(encoded_event)
            case _:
                raise InvalidEvent(encoded_event)

    @staticmethod
    def _state_event_type_from_csv(encoded_event):
        try:
            return encoded_event[2]
        except IndexError:
            raise InvalidEvent(encoded_event)

    @staticmethod
    def _variable_value_assignment_event_from_csv(encoded_event):
        return VariableValueAssignedEvent(
            EventCSVCoDec._variable_name_from_csv(encoded_event),
            EventCSVCoDec._variable_value_from_csv(encoded_event),
            EventCSVCoDec._event_timestamp_from_csv(encoded_event),
        )

    @staticmethod
    def _variable_name_from_csv(encoded_event):
        encoded_parameters = EventCSVCoDec._event_parameters_from_csv(encoded_event)
        try:
            return encoded_parameters[1]
        except IndexError:
            raise InvalidEvent(encoded_event)

    @staticmethod
    def _variable_value_from_csv(encoded_event):
        encoded_parameters = EventCSVCoDec._event_parameters_from_csv(encoded_event)
        try:
            return encoded_parameters[2]
        except IndexError:
            raise InvalidEvent(encoded_event)

    @staticmethod
    def _process_event_from_csv(encoded_event):
        process_event_type = EventCSVCoDec._process_event_type_from_csv(encoded_event)
        match process_event_type:
            case "task_started":
                return EventCSVCoDec._task_started_event_from_csv(encoded_event)
            case "task_finished":
                return EventCSVCoDec._task_finished_event_from_csv(encoded_event)
            case "checkpoint_reached":
                return EventCSVCoDec._checkpoint_reached_event_from_csv(encoded_event)
            case _:
                raise InvalidEvent(encoded_event)

    @staticmethod
    def _process_event_type_from_csv(encoded_event):
        try:
            return encoded_event[2]
        except IndexError:
            raise InvalidEvent(encoded_event)

    @staticmethod
    def _task_started_event_from_csv(encoded_event):
        return TaskStartedEvent(
            EventCSVCoDec._task_name_from_csv(encoded_event),
            EventCSVCoDec._event_timestamp_from_csv(encoded_event)
        )

    @staticmethod
    def _task_finished_event_from_csv(encoded_event):
        return TaskFinishedEvent(
            EventCSVCoDec._task_name_from_csv(encoded_event),
            EventCSVCoDec._event_timestamp_from_csv(encoded_event)
        )

    @staticmethod
    def _checkpoint_reached_event_from_csv(encoded_event):
        return CheckpointReachedEvent(
            EventCSVCoDec._checkpoint_name_from_csv(encoded_event),
            EventCSVCoDec._event_timestamp_from_csv(encoded_event),
        )

    @staticmethod
    def _task_name_from_csv(encoded_event):
        encoded_parameters = EventCSVCoDec._event_parameters_from_csv(encoded_event)
        try:
            return encoded_parameters[1]
        except IndexError:
            raise InvalidEvent(encoded_event)

    @staticmethod
    def _checkpoint_name_from_csv(encoded_event):
        encoded_parameters = EventCSVCoDec._event_parameters_from_csv(encoded_event)
        try:
            return encoded_parameters[1]
        except IndexError:
            raise InvalidEvent(encoded_event)

    # Converts a string to a component event
    @staticmethod
    def _component_event_from_csv(encoded_event):
        return ComponentEvent(
            EventCSVCoDec._component_name_from_csv(encoded_event),
            EventCSVCoDec._event_data_from_csv(encoded_event),
            EventCSVCoDec._event_timestamp_from_csv(encoded_event),
        )

    @staticmethod
    def _component_name_from_csv(encoded_event):
        try:
            return encoded_event[2]
        except IndexError:
            raise InvalidEvent(encoded_event)

    @staticmethod
    def _event_data_from_csv(encoded_event):
        try:
            event_data_as_array = encoded_event[3:]
        except IndexError:
            raise InvalidEvent(encoded_event)
        event_data_with_escaped_characters = ",".join(event_data_as_array)
        event_data = bytes(event_data_with_escaped_characters, "utf-8").decode(
            "unicode_escape"
        )
        return event_data

    @staticmethod
    def _event_type_from_csv(encoded_event):
        try:
            return encoded_event[1]
        except IndexError:
            raise InvalidEvent(encoded_event)

    @staticmethod
    def _event_timestamp_from_csv(encoded_event):
        encoded_parameters = EventCSVCoDec._event_parameters_from_csv(encoded_event)
        try:
            t = encoded_parameters[0]
        except IndexError:
            raise InvalidEvent(encoded_event)
        return int(t)

    @staticmethod
    def _event_parameters_from_csv(encoded_event):
        try:
            encoded_time = encoded_event[0]
            encoded_parameters_without_time = encoded_event[3:]
        except IndexError:
            raise InvalidEvent(encoded_event)
        encoded_parameters = [encoded_time] + encoded_parameters_without_time
        return encoded_parameters
