import logging
from faebryk.library.traits import component

from faebryk.library.trait_impl.component import (
    has_defined_footprint,
    has_defined_footprint_pinmap,
    has_defined_type_description,
    has_symmetric_footprint_pinmap,
)
from faebryk.library.kicad import (
    has_defined_kicad_ref,
    KicadFootprint,
)
logger = logging.getLogger("local_library")

from faebryk.library.core import Component, Parameter
from faebryk.library.library.components import Resistor, BJT
from faebryk.library.library.interfaces import Electrical
from faebryk.library.util import times


