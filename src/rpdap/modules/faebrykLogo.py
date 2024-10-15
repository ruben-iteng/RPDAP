# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L
from faebryk.libs.picker.picker import has_part_picked_remove

logger = logging.getLogger(__name__)


class faebrykLogo(Module):
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("LOGO")

    footprint: F.can_attach_to_footprint_symmetrically

    def __preinit__(self):
        self.footprint.attach(F.KicadFootprint("custom:faebryk_logo", pin_names=[]))

    no_pick: has_part_picked_remove
