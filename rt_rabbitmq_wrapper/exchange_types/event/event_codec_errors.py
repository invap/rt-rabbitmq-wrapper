# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

class EventTypeError(Exception):
    def __init__(self):
        super().__init__()


class EventDictError(Exception):
    def __init__(self):
        super().__init__()


class EventCSVError(Exception):
    def __init__(self):
        super().__init__()
