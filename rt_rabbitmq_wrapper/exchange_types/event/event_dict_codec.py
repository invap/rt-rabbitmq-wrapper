# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

import logging
# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)

from rt_rabbitmq_wrapper.exchange_types.event.event_codec_errors import InvalidEvent, InvalidEventDictionary
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
class EventDictCoDec:
    # Converts an event to a dictionary
    @staticmethod
    def to_dict(event):
        if isinstance(event, TimedEvent):
            return EventDictCoDec._timed_event_to_dict(event)
        elif isinstance(event, StateEvent):
            return EventDictCoDec._state_event_to_dict(event)
        elif isinstance(event, ProcessEvent):
            return EventDictCoDec._process_event_to_dict(event)
        elif isinstance(event, ComponentEvent):
            return EventDictCoDec._component_event_to_dict(event)
        else:
            logger.error(f"Invalid Event type.")
            raise InvalidEvent(event)

    # Converts a time event to a dictionary
    @staticmethod
    def _timed_event_to_dict(event):
        if isinstance(event, ClockPauseEvent):
            return EventDictCoDec._clock_pause_event_to_dict(event)
        elif isinstance(event, ClockResetEvent):
            return EventDictCoDec._clock_reset_event_to_dict(event)
        elif isinstance(event, ClockResumeEvent):
            return EventDictCoDec._clock_resume_event_to_dict(event)
        elif isinstance(event, ClockStartEvent):
            return EventDictCoDec._clock_start_event_to_dict(event)
        else:
            logger.error(f"Invalid TimeEvent subtype.")
            raise InvalidEvent(event)

    @staticmethod
    def _clock_pause_event_to_dict(event):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "clock_name": event.clock_name()
        }

    @staticmethod
    def _clock_reset_event_to_dict(event):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "clock_name": event.clock_name()
        }

    @staticmethod
    def _clock_resume_event_to_dict(event):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "clock_name": event.clock_name()
        }

    @staticmethod
    def _clock_start_event_to_dict(event):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "clock_name": event.clock_name()
        }

    # Converts a state event to a dictionary
    @staticmethod
    def _state_event_to_dict(event):
        if isinstance(event, VariableValueAssignedEvent):
            return EventDictCoDec._variable_value_assigned_event_to_dict(event)
        else:
            logger.error(f"Invalid TimeEvent subtype.")
            raise InvalidEvent(event)

    @staticmethod
    def _variable_value_assigned_event_to_dict(event):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "variable_name": event.variable_name(),
            "variable_value": event.variable_value()
        }

    # Converts a process event to a dictionary
    @staticmethod
    def _process_event_to_dict(event):
        if isinstance(event, TaskStartedEvent):
            return EventDictCoDec._task_started_event_to_dict(event)
        elif isinstance(event, TaskFinishedEvent):
            return EventDictCoDec._task_finished_event_to_dict(event)
        elif isinstance(event, CheckpointReachedEvent):
            return EventDictCoDec._checkpoint_reached_event_to_dict(event)
        else:
            logger.error(f"Invalid TimeEvent subtype.")
            raise InvalidEvent(event)

    @staticmethod
    def _task_started_event_to_dict(event):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "name": event.name()
        }

    @staticmethod
    def _task_finished_event_to_dict(event):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "name": event.name()
        }

    @staticmethod
    def _checkpoint_reached_event_to_dict(event):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "name": event.name()
        }

    # Converts a component event to a dictionary
    @staticmethod
    def _component_event_to_dict(event):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "component_name": event.component_name(),
            "data": event.data()
        }

    # Converts a dictionary to an event
    @staticmethod
    def from_dict(event_dict):
        try:
            match event_dict["event_type"]:
                case "timed_event":
                    event = EventDictCoDec._timed_event_from_dict(event_dict)
                case "state_event":
                    event = EventDictCoDec._state_event_from_dict(event_dict)
                case "process_event":
                    event = EventDictCoDec._process_event_from_dict(event_dict)
                case "component_event":
                    event = EventDictCoDec._component_event_from_dict(event_dict)
                case _:
                    logger.error(f"Invalid Event type.")
                    raise InvalidEventDictionary(event_dict)
        except KeyError:
            logger.error(f"Invalid dictionary key set for building a Event.")
            raise InvalidEventDictionary(event_dict)
        else:
            return event

    # Converts a dictionary to a timed event
    @staticmethod
    def _timed_event_from_dict(event_dict):
        try:
            match event_dict["event_subtype"]:
                case "clock_pause":
                    event = ClockPauseEvent(event_dict["clock_name"], event_dict["timestamp"])
                case "clock_reset":
                    event = ClockResetEvent(event_dict["clock_name"], event_dict["timestamp"])
                case "clock_resume":
                    event = ClockResumeEvent(event_dict["clock_name"], event_dict["timestamp"])
                case "clock_start":
                    event = ClockStartEvent(event_dict["clock_name"], event_dict["timestamp"])
                case _:
                    logger.error(f"Invalid TimeEvent subtype.")
                    raise InvalidEventDictionary(event_dict)
        except KeyError:
            logger.error(f"Invalid dictionary key set for building a TimedEvent.")
            raise InvalidEventDictionary(event_dict)
        else:
            return event

    # Converts a dictionary to a state event
    @staticmethod
    def _state_event_from_dict(event_dict):
        try:
            match event_dict["event_subtype"]:
                case "variable_value_assigned":
                    event = VariableValueAssignedEvent(event_dict["variable_name"], event_dict["variable_value"], event_dict["timestamp"])
                case _:
                    logger.error(f"Invalid StateEvent subtype.")
                    raise InvalidEventDictionary(event_dict)
        except KeyError:
            logger.error(f"Invalid dictionary key set for building a StateEvent.")
            raise InvalidEventDictionary(event_dict)
        else:
            return event

    # Converts a dictionary to a process event
    @staticmethod
    def _process_event_from_dict(event_dict):
        try:
            match event_dict["event_subtype"]:
                case "task_started":
                    event = TaskStartedEvent(event_dict["name"], event_dict["timestamp"])
                case "task_finished":
                    event = TaskFinishedEvent(event_dict["name"], event_dict["timestamp"])
                case "checkpoint_reached":
                    event = CheckpointReachedEvent(event_dict["name"], event_dict["timestamp"])
                case _:
                    logger.error(f"Invalid ProcessEvent subtype.")
                    raise InvalidEventDictionary(event_dict)
        except KeyError:
            logger.error(f"Invalid dictionary key set for building a ProcessEvent.")
            raise InvalidEventDictionary(event_dict)
        else:
            return event

    # Converts a dictionary to a component event
    @staticmethod
    def _component_event_from_dict(event_dict):
        try:
            event = ComponentEvent(event_dict["component_name"], event_dict["data"], event_dict["timestamp"])
        except KeyError:
            logger.error(f"Invalid dictionary key set for building a ComponentEvent.")
            raise InvalidEventDictionary(event_dict)
        else:
            return event
