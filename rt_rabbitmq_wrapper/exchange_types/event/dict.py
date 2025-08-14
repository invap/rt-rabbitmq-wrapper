# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

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
        return _component_event_to_dict(event)
    elif isinstance(event, TimedEvent):
        return _timed_event_to_dict(event)
    elif isinstance(event, StateEvent):
        return _state_event_to_dict(event)
    elif isinstance(event, ProcessEvent):
        return _process_event_to_dict(event)
    else:
        logger.error(f"Invalid Event type.")
        raise EventError()

# Converts a component event to a dictionary
def _component_event_to_dict(event):
    return {
        "timestamp": event.timestamp(),
        "event_type": event.event_type(),
        "component_name": event.component_name(),
        "data": event.data()
    }

# Converts a time event to a dictionary
def _timed_event_to_dict(event):
    if isinstance(event, ClockPauseEvent):
        return _clock_pause_event_to_dict(event)
    elif isinstance(event, ClockResetEvent):
        return _clock_reset_event_to_dict(event)
    elif isinstance(event, ClockResumeEvent):
        return _clock_resume_event_to_dict(event)
    elif isinstance(event, ClockStartEvent):
        return _clock_start_event_to_dict(event)
    else:
        logger.error(f"Invalid TimeEvent subtype.")
        raise EventError()

def _clock_pause_event_to_dict(event):
    return {
        "timestamp": event.timestamp(),
        "event_type": event.event_type(),
        "event_subtype": event.event_subtype(),
        "clock_name": event.clock_name()
    }

def _clock_reset_event_to_dict(event):
    return {
        "timestamp": event.timestamp(),
        "event_type": event.event_type(),
        "event_subtype": event.event_subtype(),
        "clock_name": event.clock_name()
    }

def _clock_resume_event_to_dict(event):
    return {
        "timestamp": event.timestamp(),
        "event_type": event.event_type(),
        "event_subtype": event.event_subtype(),
        "clock_name": event.clock_name()
    }

def _clock_start_event_to_dict(event):
    return {
        "timestamp": event.timestamp(),
        "event_type": event.event_type(),
        "event_subtype": event.event_subtype(),
        "clock_name": event.clock_name()
    }

# Converts a state event to a dictionary
def _state_event_to_dict(event):
    if isinstance(event, VariableValueAssignedEvent):
        return _variable_value_assigned_event_to_dict(event)
    else:
        logger.error(f"Invalid TimeEvent subtype.")
        raise EventError()

def _variable_value_assigned_event_to_dict(event):
    return {
        "timestamp": event.timestamp(),
        "event_type": event.event_type(),
        "event_subtype": event.event_subtype(),
        "variable_name": event.variable_name(),
        "variable_value": event.variable_value()
    }

# Converts a process event to a dictionary
def _process_event_to_dict(event):
    if isinstance(event, TaskStartedEvent):
        return _task_started_event_to_dict(event)
    elif isinstance(event, TaskFinishedEvent):
        return _task_finished_event_to_dict(event)
    elif isinstance(event, CheckpointReachedEvent):
        return _checkpoint_reached_event_to_dict(event)
    else:
        logger.error(f"Invalid TimeEvent subtype.")
        raise EventError()

def _task_started_event_to_dict(event):
    return {
        "timestamp": event.timestamp(),
        "event_type": event.event_type(),
        "event_subtype": event.event_subtype(),
        "name": event.name()
    }

def _task_finished_event_to_dict(event):
    return {
        "timestamp": event.timestamp(),
        "event_type": event.event_type(),
        "event_subtype": event.event_subtype(),
        "name": event.name()
    }

def _checkpoint_reached_event_to_dict(event):
    return {
        "timestamp": event.timestamp(),
        "event_type": event.event_type(),
        "event_subtype": event.event_subtype(),
        "name": event.name()
    }


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
        event = ComponentEvent(dict["component_name"], dict["data"], dict["timestamp"])
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a ComponentEvent.")
        raise EventError()
    else:
        return event

# Converts a dictionary to a timed event
def _timed_event_from_dict(dict):
    try:
        match dict["event_subtype"]:
            case "clock_pause":
                event = ClockPauseEvent(dict["clock_name"], dict["timestamp"])
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
