# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

class Specification:
    def __init__(self, property_name, timestamp, spec):
        self._property_name = property_name
        self._timestamp = timestamp
        self._spec = spec

    @property
    def property_name(self):
        return self._property_name

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def specification(self):
        return self._spec


class PySpecification(Specification):
    def __init__(self, property_name, timestamp, spec) -> None:
        super().__init__(property_name, timestamp, spec)


class SymPySpecification(Specification):
    def __init__(self, property_name, timestamp, spec) -> None:
        super().__init__(property_name, timestamp, spec)


class SMT2Specification(Specification):
    def __init__(self, property_name, timestamp, spec) -> None:
        super().__init__(property_name, timestamp, spec)
