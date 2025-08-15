# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from rt_rabbitmq_wrapper.exchange_types.event.task_event import TaskEvent


class TaskFinishedEvent(TaskEvent):
    def __init__(self, name, time) -> None:
        super().__init__(name, time)

    @staticmethod
    def event_subtype():
        return "task_finished"

    def process_with(self, monitor):
        return monitor.process_task_finished(self)
