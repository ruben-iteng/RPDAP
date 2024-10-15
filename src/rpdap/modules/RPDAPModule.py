# This file is part of the faebryk project
# SPDX-License-Identifier: MIT


import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.exporters.pcb.layout.extrude import LayoutExtrude
from faebryk.exporters.pcb.layout.typehierarchy import LayoutTypeHierarchy
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


class RPDAPModule(Module):
    usb_connector = L.f_field(F.Header)(horizonal_pin_count=4, vertical_pin_count=1)
    data_connector = L.f_field(F.Header)(horizonal_pin_count=5, vertical_pin_count=2)

    usb: F.USB2_0
    swd: F.SWD
    gnd_detect: F.ElectricLogic
    uart: F.UART_Base
    device_power: F.ElectricPower

    @L.rt_field
    def has_defined_layout(self):
        # pcb layout
        Point = F.has_pcb_position.Point
        L = F.has_pcb_position.layer_type
        LVL = LayoutTypeHierarchy.Level

        layouts = [
            LVL(
                mod_type=F.Header,
                layout=LayoutExtrude(
                    base=Point((0, (2.54 / 2), 0, L.NONE)),
                    vector=(0, 50 - (1.5 * 2.54), 0),
                    reverse_order=True,
                ),
            ),
        ]
        return F.has_pcb_layout_defined(LayoutTypeHierarchy(layouts))

    def __preinit__(self):
        # ----------------------------------------
        #               Aliasses
        # ----------------------------------------
        vbus = self.usb.usb_if.buspower

        # ----------------------------------------
        #            parametrization
        # ----------------------------------------
        self.usb_connector.pin_pitch.merge(2.54 * P.mm)
        self.data_connector.pin_pitch.merge(2.54 * P.mm)
        self.usb_connector.spacer_height.merge(F.Range.from_center_rel(8.5 * P.mm, 0.1))
        self.data_connector.spacer_height.merge(
            F.Range.from_center_rel(8.5 * P.mm, 0.1)
        )
        self.usb_connector.pin_type.merge(F.Header.PinType.FEMALE)
        self.data_connector.pin_type.merge(F.Header.PinType.FEMALE)
        self.usb_connector.angle.merge(F.Header.Angle.STRAIGHT)
        self.data_connector.angle.merge(F.Header.Angle.STRAIGHT)

        # ----------------------------------------
        #               Connections
        # ----------------------------------------
        F.ElectricLogic.connect_all_module_references(self, gnd_only=True)
        F.ElectricLogic.connect_all_module_references(
            self, exclude=[self.usb]
        ).voltage.merge(F.Range(1.7 * P.V, 5.5 * P.V))

        # USB header
        # power
        vbus.lv.connect(self.usb_connector.contact[3])
        vbus.hv.connect(self.usb_connector.contact[0])
        # usb
        self.usb.usb_if.d.n.signal.connect(self.usb_connector.contact[1])
        self.usb.usb_if.d.p.signal.connect(self.usb_connector.contact[2])

        # target header
        # data connector UART connections
        self.uart.rx.signal.connect(self.data_connector.contact[4])
        self.uart.tx.signal.connect(self.data_connector.contact[6])
        # data connector SWD connections
        self.swd.clk.signal.connect(self.data_connector.contact[3])
        self.swd.dio.signal.connect(self.data_connector.contact[1])
        self.swd.swo.signal.connect(self.data_connector.contact[5])
        self.swd.reset.signal.connect(self.data_connector.contact[9])
        # data connector GND detect connections
        self.gnd_detect.signal.connect(self.data_connector.contact[8])
        self.device_power.lv.connect(self.data_connector.contact[2])
        self.device_power.hv.connect(self.data_connector.contact[0])
