# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from rt_rabbitmq_wrapper.exchange_types.event.event import Event, NoEventSubtypeError


class ComponentEvent(Event):
    def __init__(self, component_name, data, timestamp) -> None:
        super().__init__(timestamp)
        self._component_name = component_name
        self._data = data

    def component_name(self):
        return self._component_name

    def data(self):
        return self._data

    @staticmethod
    def event_type():
        return "component_event"

    @staticmethod
    def event_subtype():
        raise NoEventSubtypeError

    def process_with(self, monitor):
        return monitor.process_component_event(self)

    def __str__(self):
        return f"(timestamp: {self.timestamp}) - component_event(component_name: {self._component_name}, data: {self._data})"

    def __repr__(self):
        return f"(timestamp: {self.timestamp}) - component_event(component_name: {self._component_name}, data: {self._data})"
