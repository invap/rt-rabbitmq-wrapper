# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from rt_rabbitmq_wrapper.exchange_types.event.event import Event


class ProcessEvent(Event):
    def __init__(self, timestamp) -> None:
        super().__init__(timestamp)

    @staticmethod
    def event_type():
        return "process_event"
