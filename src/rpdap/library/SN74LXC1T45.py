# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

from faebryk.core.core import Module
from faebryk.library.can_attach_to_footprint_via_pinmap import (
    can_attach_to_footprint_via_pinmap,
)
from faebryk.library.can_be_decoupled import can_be_decoupled
from faebryk.library.ElectricLogic import ElectricLogic
from faebryk.library.ElectricPower import ElectricPower
from faebryk.library.can_bridge_defined import can_bridge_defined
from faebryk.library.has_datasheet_defined import has_datasheet_defined
from faebryk.library.has_designator_prefix_defined import has_designator_prefix_defined
from faebryk.library.KicadFootprint import KicadFootprint
from faebryk.library.Range import Range
from faebryk.libs.units import P
from faebryk.libs.util import times

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

    @classmethod
    def NODES(cls):
        # submodules
        class _NODES(super().NODES()):
            pass

        return _NODES

    @classmethod
    def PARAMS(cls):
        # parameters
        class _PARAMS(super().PARAMS()):
            pass

        return _PARAMS

    @classmethod
    def IFS(cls):
        # interfaces
        class _IFS(super().IFS()):
            dir = ElectricLogic()
            io = times(2, ElectricLogic)
            power = times(2, ElectricPower)

        return _IFS

    def __init__(self):
        # boilerplate
        super().__init__()
        self.IFs = self.IFS()(self)
        self.PARAMs = self.PARAMS()(self)
        self.NODEs = self.NODES()(self)

        # parameters
        for pwr in self.IFs.power:
            pwr.PARAMs.voltage.merge(Range(1.1 * P.V, 5.5 * P.V))
            pwr.get_trait(can_be_decoupled).decouple()

        # connections
        self.IFs.power[0].IFs.lv.connect(self.IFs.power[1].IFs.lv)

        # traits
        self.add_trait(can_bridge_defined(self.IFs.io[0], self.IFs.io[1]))

        self.add_trait(
            has_datasheet_defined("https://www.ti.com/lit/ds/symlink/sn74lxc1t45.pdf")
        )

        self.add_trait(has_designator_prefix_defined("U"))

        self.add_trait(
            can_attach_to_footprint_via_pinmap(
                pinmap={
                    "1": self.IFs.power[0].IFs.hv,
                    "2": self.IFs.power[0].IFs.lv,
                    "3": self.IFs.io[0].IFs.signal,
                    "4": self.IFs.io[1].IFs.signal,
                    "5": self.IFs.dir.IFs.signal,
                    "6": self.IFs.power[1].IFs.hv,
                }
            )
        ).attach(
            KicadFootprint(
                kicad_identifier="Package_TO_SOT_SMD:SOT-23-6",
                pin_names=["1", "2", "3", "4", "5", "6"],
            )
        )
