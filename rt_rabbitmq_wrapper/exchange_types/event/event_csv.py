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
def event_to_csv(event):
    if isinstance(event, ComponentEvent):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.component_name() + "," + event.data()
    elif isinstance(event, TimedEvent):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.clock_name()
    elif isinstance(event, StateEvent):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.variable_name() + "," + event.variable_value()
    elif isinstance(event, ProcessEvent):
        return str(event.timestamp()) + "," + event.event_type() + "," + event.event_subtype() + "," + event.name()
    else:
        logger.error(f"Invalid Event type.")
        raise EventError()


# Converts a string to an event
def event_from_csv(string):
    split_str = string.split(",")
    try:
        match split_str[1]:
            case "component_event":
                event = _component_event_from_csv(string)
            case "timed_event":
                event = _timed_event_from_csv(string)
            case "state_event":
                event = _state_event_from_csv(string)
            case "process_event":
                event = _process_event_from_csv(string)
            case _:
                logger.error(f"Invalid Event type.")
                raise EventError()
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a Event.")
        raise EventError()
    else:
        return event

# Converts a dictionary to a component event
def _component_event_from_csv(string):
    split_str = string.split(",")
    try:
        event = ComponentEvent(split_str[2], split_str[3], split_str[0])
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a ComponentEvent.")
        raise EventError()
    else:
        return event

# Converts a dictionary to a timed event
def _timed_event_from_csv(string):
    split_str = string.split(",")
    try:
        match dict["event_subtype"]:
            case "clock_pause":
                event = ClockPauseEvent(split_str[3], split_str[0])
            case "clock_reset":
                event = ClockResetEvent(split_str[3], split_str[0])
            case "clock_resume":
                event = ClockResumeEvent(split_str[3], split_str[0])
            case "clock_start":
                event = ClockStartEvent(split_str[3], split_str[0])
            case _:
                logger.error(f"Invalid TimeEvent subtype.")
                raise EventError()
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a TimedEvent.")
        raise EventError()
    else:
        return event

# Converts a dictionary to a state event
def _state_event_from_csv(string):
    split_str = string.split(",")
    try:
        match dict["event_subtype"]:
            case "variable_value_assigned":
                event = VariableValueAssignedEvent(split_str[3], split_str[4], split_str[0])
            case _:
                logger.error(f"Invalid StateEvent subtype.")
                raise EventError()
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a StateEvent.")
        raise EventError()
    else:
        return event

# Converts a dictionary to a process event
def _process_event_from_csv(string):
    split_str = string.split(",")
    try:
        match dict["event_subtype"]:
            case "task_started":
                event = TaskStartedEvent(split_str[3], split_str[0])
            case "task_finished":
                event = TaskFinishedEvent(split_str[3], split_str[0])
            case "checkpoint_reached":
                event = CheckpointReachedEvent(split_str[3], split_str[0])
            case _:
                logger.error(f"Invalid ProcessEvent subtype.")
                raise EventError()
    except KeyError:
        logger.error(f"Invalid dictionary key set for building a ProcessEvent.")
        raise EventError()
    else:
        return event
