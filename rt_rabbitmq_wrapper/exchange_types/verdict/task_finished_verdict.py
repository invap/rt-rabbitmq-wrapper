# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

from rt_rabbitmq_wrapper.exchange_types.verdict.process_verdict import ProcessVerdict


class TaskFinishedVerdict(ProcessVerdict):
    def __init__(self, timestamp, name, verdict) -> None:
        super().__init__(timestamp, verdict)
        self._name = name

    @property
    def task_name(self):
        return self._name

    @staticmethod
    def verdict_subtype():
        return "task_finished"

    def __str__(self):
        return f"(timestamp: {self.timestamp}) - task_finished(name: {self.task_name}, verdict: {self.verdict.name})"

    def __repr__(self):
        return f"(timestamp: {self.timestamp}) - task_finished(name: {self.task_name}, verdict: {self.verdict.name})"
