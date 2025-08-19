# Copyright (c) 2024 Fundacion Sadosky, info@fundacionsadosky.org.ar
# Copyright (c) 2024 INVAP, open@invap.com.ar
# SPDX-License-Identifier: AGPL-3.0-or-later OR Fundacion-Sadosky-Commercial

import logging
# Create a logger for the RabbitMQ utility component
logger = logging.getLogger(__name__)


from rt_rabbitmq_wrapper.exchange_types.specification.specification_codec_errors import (
    SpecificationTypeError,
    SpecificationDictError
)
from rt_rabbitmq_wrapper.exchange_types.specification.specification import (
    PySpecification,
    SymPySpecification,
    SMT2Specification
)

# Raises: EventTypeError()
class SpecificationDictCoDec:
    # Converts a specification to a dictionary
    @staticmethod
    def to_dict(spec):
        if isinstance(spec, PySpecification):
            return SpecificationDictCoDec._pyspecification_to_dict(spec)
        elif isinstance(spec, SymPySpecification):
            return SpecificationDictCoDec._sympyspecification_to_dict(spec)
        elif isinstance(spec, SMT2Specification):
            return SpecificationDictCoDec._smt2specification_to_dict(spec)
        else:
            logger.error(f"Invalid specification type.")
            raise SpecificationTypeError()

    @staticmethod
    def _pyspecification_to_dict(spec):
        return {
            "spec_type": "py",
            "timestamp": spec.timestamp,
            "property_name": spec.property_name,
            "specification": spec.specification
        }

    @staticmethod
    def _sympyspecification_to_dict(spec):
        return {
            "spec_type": "sympy",
            "timestamp": spec.timestamp,
            "property_name": spec.property_name,
            "specification": spec.specification
        }

    @staticmethod
    def _smt2specification_to_dict(spec):
        return {
            "spec_type": "smt2",
            "timestamp": spec.timestamp,
            "property_name": spec.property_name,
            "specification": spec.specification
        }

    # Converts a dictionary to a specification
    @staticmethod
    def from_dict(specification_dict):
        try:
            match specification_dict["spec_type"]:
                case "py":
                    specification = SpecificationDictCoDec._pyspecification_from_dict(specification_dict)
                case "sympy":
                    specification = SpecificationDictCoDec._sympyspecification_from_dict(specification_dict)
                case "smt2":
                    specification = SpecificationDictCoDec._smt2specification_from_dict(specification_dict)
                case _:
                    logger.error(f"Invalid specification type.")
                    raise SpecificationDictError()
        except KeyError:
            logger.error(f"Invalid dictionary key set for building a specification.")
            raise SpecificationDictError()
        else:
            return specification

    @staticmethod
    def _pyspecification_from_dict(specification_dict):
        return PySpecification(specification_dict["property_name"], specification_dict["timestamp"], specification_dict["specification"])

    @staticmethod
    def _sympyspecification_from_dict(specification_dict):
        return SymPySpecification(specification_dict["property_name"], specification_dict["timestamp"], specification_dict["specification"])

    @staticmethod
    def _smt2specification_from_dict(specification_dict):
        return SMT2Specification(specification_dict["property_name"], specification_dict["timestamp"], specification_dict["specification"])
