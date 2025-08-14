# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

import logging
# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)

from rt_rabbitmq_wrapper.exchange_types.event.event import (
    Event,
    EventError
)
from rt_rabbitmq_wrapper.exchange_types.event.component_event import ComponentEvent
from rt_rabbitmq_wrapper.exchange_types.event.timed_event import TimedEvent
from rt_rabbitmq_wrapper.exchange_types.event.clock_pause_event import ClockPauseEvent
from rt_rabbitmq_wrapper.exchange_types.event.clock_reset_event import ClockResetEvent
from rt_rabbitmq_wrapper.exchange_types.event.clock_resume_event import ClockResumeEvent
from rt_rabbitmq_wrapper.exchange_types.event.clock_start_event import ClockStartEvent
from rt_rabbitmq_wrapper.exchange_types.event.process_event import ProcessEvent
from rt_rabbitmq_wrapper.exchange_types.event.task_event import TaskEvent
from rt_rabbitmq_wrapper.exchange_types.event.task_started_event import TaskStartedEvent
from rt_rabbitmq_wrapper.exchange_types.event.task_finished_event import TaskFinishedEvent
from rt_rabbitmq_wrapper.exchange_types.event.checkpoint_reached_event import CheckpointReachedEvent
from rt_rabbitmq_wrapper.exchange_types.event.state_event import StateEvent
from rt_rabbitmq_wrapper.exchange_types.event.variable_value_assigned_event import VariableValueAssignedEvent


# Converts an event to a dictionary
def event_to_dict(event):
    if isinstance(event, ComponentEvent):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "component_name": event.component_name(),
            "data": event.data()
        }
    elif isinstance(event, TimedEvent):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "clock_name": event.clock_name()
        }
    elif isinstance(event, StateEvent):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "variable_name": event.variable_name(),
            "variable_value": event.variable_value()
        }
    elif isinstance(event, ProcessEvent):
        return {
            "timestamp": event.timestamp(),
            "event_type": event.event_type(),
            "event_subtype": event.event_subtype(),
            "name": event.name()
        }
    else:
        logger.error(f"Invalid Event type.")
        raise EventError()


# Converts a dictionary to an event
def event_from_dict(dict):
    try:
        match dict["event_type"]:
            case "component_event":
                event = _component_event_from_dict(dict)
            case "timed_event":
                event = _timed_event_from_dict(dict)
            case "state_event":
                event = _state_event_from_dict(dict)
            case "process_event":
                event = _process_event_from_dict(dict)
            case _:
                logger.error(f"Invalid Event type.")
                raise EventError()
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a Event.")
        raise EventError()
    else:
        return event

# Converts a dictionary to a component event
def _component_event_from_dict(dict):
    try:
        str = str(dict["timestamp"])+","+dict["component_name"]+","+dict["data"]
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a ComponentEvent.")
        raise EventError()
    else:
        return str

# Converts a dictionary to a timed event
def _timed_event_from_dict(dict):
    try:
        match dict["event_subtype"]:
            case "clock_pause":
                event = str(dict["timestamp"])+","+""+ClockPauseEvent(dict["clock_name"], )
            case "clock_reset":
                event = ClockResetEvent(dict["clock_name"], dict["timestamp"])
            case "clock_resume":
                event = ClockResumeEvent(dict["clock_name"], dict["timestamp"])
            case "clock_start":
                event = ClockStartEvent(dict["clock_name"], dict["timestamp"])
            case _:
                logger.error(f"Invalid TimeEvent subtype.")
                raise EventError()
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a TimedEvent.")
        raise EventError()
    else:
        return event

# Converts a dictionary to a state event
def _state_event_from_dict(dict):
    try:
        match dict["event_subtype"]:
            case "variable_value_assigned":
                event = VariableValueAssignedEvent(dict["variable_name"], dict["variable_value"], dict["timestamp"])
            case _:
                logger.error(f"Invalid StateEvent subtype.")
                raise EventError()
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a StateEvent.")
        raise EventError()
    else:
        return event

# Converts a dictionary to a process event
def _process_event_from_dict(dict):
    try:
        match dict["event_subtype"]:
            case "task_started":
                event = TaskStartedEvent(dict["name"], dict["timestamp"])
            case "task_finished":
                event = TaskFinishedEvent(dict["name"], dict["timestamp"])
            case "checkpoint_reached":
                event = CheckpointReachedEvent(dict["name"], dict["timestamp"])
            case _:
                logger.error(f"Invalid ProcessEvent subtype.")
                raise EventError()
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a ProcessEvent.")
        raise EventError()
    else:
        return event
