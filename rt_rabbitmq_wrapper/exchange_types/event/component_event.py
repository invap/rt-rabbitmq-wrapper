# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from rt_rabbitmq_wrapper.exchange_types.event.event import Event

class NoSubtypeError(Exception):
    def __init__(self):
        super().__init__()


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
        raise NoSubtypeError

    @staticmethod
    def decode_with(decoder, encoded_event):
        return decoder.decode_component_event(encoded_event)

    def process_with(self, monitor):
        return monitor.process_component_event(self)

    def serialized(self):
        return (
            f"{self.timestamp()},{self.event_type()},{self.component_name()},{self.data()}"
        )
