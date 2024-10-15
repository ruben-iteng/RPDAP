# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L
from faebryk.libs.units import P

logger = logging.getLogger(__name__)


class SN74LXC1T45(Module):
    """
    he SN74LXC1T45 is a 1-bit, dual-supply
    noninverting bidirectional voltage level translation
    device. The I/O pin A and control pin (DIR) are
    referenced to VCCA logic levels, and the I/O pin B are
    referenced to VCCB logic levels. The A pin is able to
    accept I/O voltages ranging from 1.1 V to 5.5 V, while
    the B pin can accept I/O voltages from 1.1 V to 5.5 V.
    A high on DIR allows data transmission from A to B
    and a low on DIR allows data transmission from B to
    A.
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    dir = F.ElectricLogic()
    io = L.list_field(2, F.ElectricLogic)
    power = L.list_field(2, F.ElectricPower)

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    @L.rt_field
    def can_bridge(self):
        return F.can_bridge_defined(self.io[0], self.io[1])

    @L.rt_field
    def datasheet(self):
        return F.has_datasheet_defined(
            "https://www.ti.com/lit/ds/symlink/sn74lxc1t45.pdf"
        )

    designator_prefix = L.f_field(F.has_designator_prefix_defined)(
        F.has_designator_prefix.Prefix.U
    )

    @L.rt_field
    def can_attach_to_footprint(self):
        return F.can_attach_to_footprint_via_pinmap(
            pinmap={
                "1": self.power[0].hv,
                "2": self.power[0].lv,
                "3": self.io[0].signal,
                "4": self.io[1].signal,
                "5": self.dir.signal,
                "6": self.power[1].hv,
            }
        )

    def __preinit__(self):
        self.can_attach_to_footprint.attach(
            F.KicadFootprint(
                kicad_identifier="Package_TO_SOT_SMD:SOT-23-6",
                pin_names=["1", "2", "3", "4", "5", "6"],
            )
        )

        for pwr in self.power:
            pwr.voltage.merge(F.Range(1.1 * P.V, 5.5 * P.V))
            pwr.get_trait(F.can_be_decoupled).decouple()

        # connections
        self.power[0].lv.connect(self.power[1].lv)
