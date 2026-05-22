# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from rt_rabbitmq_wrapper.exchange_types.event.process_event import ProcessEvent


class CheckpointReachedEvent(ProcessEvent):
    def __init__(self, name, time) -> None:
        super().__init__(time)
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def event_subtype(self):
        return "checkpoint_reached"

    def process_with(self, monitor):
        return monitor.process_checkpoint_reached(self)

    def __str__(self):
        return f"(timestamp: {self.timestamp}) - checkpoint_reached(name: {self.name})"

    def __repr__(self):
        return f"(timestamp: {self.timestamp}) - checkpoint_reached(name: {self.name})"
