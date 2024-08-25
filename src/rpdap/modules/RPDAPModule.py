# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.core import Module
from faebryk.exporters.pcb.layout.absolute import LayoutAbsolute
from faebryk.exporters.pcb.layout.typehierarchy import LayoutTypeHierarchy

from rpdap.modules.MountingSlot import MountingSlot
from rpdap.modules.SFPEdgeConnector import SFPEdgeConnector

logger = logging.getLogger(__name__)


class RPDAPModule(Module):
    @classmethod
    def NODES(cls):
        # submodules
        class _NODES(super().NODES()):
            cardedge_connector = SFPEdgeConnector()
            keys = MountingSlot()

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
            usb = F.USB2_0()
            swd = F.SWD()
            gnd_detect = F.Electrical()
            uart = F.UART_Base()

        return _IFS

    def __init__(self):
        # boilerplate
        super().__init__()
        self.IFs = self.IFS()(self)
        self.PARAMs = self.PARAMS()(self)
        self.NODEs = self.NODES()(self)

        # aliases
        vbus = self.IFs.usb.IFs.usb_if.IFs.buspower
        gnd = vbus.IFs.lv

        # connections
        # power
        for gnd_pin in [0, 9, 10, 13, 16, 19]:
            gnd.connect(self.NODEs.cardedge_connector.IFs.unnamed[gnd_pin])
        for power_pin in [14, 15]:
            vbus.IFs.hv.connect(self.NODEs.cardedge_connector.IFs.unnamed[power_pin])
        # swd
        self.IFs.swd.IFs.clk.IFs.signal.connect(
            self.NODEs.cardedge_connector.IFs.unnamed[18]
        )
        self.IFs.swd.IFs.dio.IFs.signal.connect(
            self.NODEs.cardedge_connector.IFs.unnamed[19]
        )
        self.IFs.swd.IFs.swo.IFs.signal.connect(
            self.NODEs.cardedge_connector.IFs.unnamed[1]
        )
        self.IFs.swd.IFs.reset.IFs.signal.connect(
            self.NODEs.cardedge_connector.IFs.unnamed[2]
        )
        # uart
        self.IFs.uart.IFs.tx.IFs.signal.connect(
            self.NODEs.cardedge_connector.IFs.unnamed[3]
        )
        self.IFs.uart.IFs.rx.IFs.signal.connect(
            self.NODEs.cardedge_connector.IFs.unnamed[4]
        )
        # gnd detect
        self.IFs.gnd_detect.connect(self.NODEs.cardedge_connector.IFs.unnamed[5])

        # usb
        self.IFs.usb.IFs.usb_if.IFs.d.IFs.p.connect(
            self.NODEs.cardedge_connector.IFs.unnamed[12]
        )
        self.IFs.usb.IFs.usb_if.IFs.d.IFs.n.connect(
            self.NODEs.cardedge_connector.IFs.unnamed[11]
        )

        # traits

        # pcb layout
        Point = F.has_pcb_position.Point
        L = F.has_pcb_position.layer_type
        LVL = LayoutTypeHierarchy.Level

        layouts = [
            LVL(
                mod_type=MountingSlot,
                layout=LayoutAbsolute(Point((0, 0, 0, L.NONE))),
            ),
            LVL(
                mod_type=SFPEdgeConnector,
                layout=LayoutAbsolute(Point((0, 45, 0, L.NONE))),
            ),
        ]
        self.add_trait(F.has_pcb_layout_defined(LayoutTypeHierarchy(layouts)))
