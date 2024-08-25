# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.core import Module
from faebryk.libs.brightness import TypicalLuminousIntensity
from faebryk.libs.util import times

from rpdap.library.Connector import Connector
from rpdap.library.SN74LXC1T45 import SN74LXC1T45
from rpdap.modules.faebrykLogo import faebrykLogo
from rpdap.modules.RPDAPModule import RPDAPModule

logger = logging.getLogger(__name__)

"""
This file is for the top-level application modules.
This should be the entrypoint for collaborators to start in to understand your project.
Treat it as the high-level design of your project.
Avoid putting any generic or reusable application modules here.
Avoid putting any low-level modules or parameter specializations here.
"""


class MyApp(Module):
    def __init__(self) -> None:
        super().__init__()

        # modules ------------------------------------
        class _NODEs(Module.NODES()):
            rpdap_module = RPDAPModule()
            faebryk_logo = faebrykLogo()
            mcu = F.RP2040_Reference_Design()
            vcp_status_led = F.PoweredLED()
            mcu_swd_connector = Connector()
            level_shifter = times(4, SN74LXC1T45)

        class _PARAMs(Module.PARAMS()):
            pass

        self.NODEs = _NODEs(self)
        self.PARAMs = _PARAMs(self)

        # aliases ------------------------------------
        vbus = self.NODEs.rpdap_module.IFs.usb.IFs.usb_if.IFs.buspower
        gnd = vbus.IFs.lv
        v3_3 = self.NODEs.mcu.NODEs.ldo.IFs.power_out
        usb = self.NODEs.rpdap_module.IFs.usb
        target_swd = self.NODEs.rpdap_module.IFs.swd
        mcu_swd = self.NODEs.mcu.NODEs.rp2040.IFs.swd
        uart = self.NODEs.rpdap_module.IFs.uart

        # net names ----------------------------------
        nets = {
            "vbus": vbus.IFs.hv,
            "3v3": v3_3.IFs.hv,
            "gnd": gnd,
            "usb_P": usb.IFs.usb_if.IFs.d.IFs.p,
            "usb_N": usb.IFs.usb_if.IFs.d.IFs.n,
            "swd_clk": target_swd.IFs.clk,
            "swd_dio": target_swd.IFs.dio,
            "swd_swo": target_swd.IFs.swo,
            "swd_reset": target_swd.IFs.reset,
        }
        for net_name, mif in nets.items():
            assert isinstance(
                mif, F.Electrical
            ), f"You are trying to give a non-electrical interface: {mif}, a net name: {net_name}"  # noqa E501
            net = F.Net.with_name(net_name)
            net.IFs.part_of.connect(mif)

        # parametrization ----------------------------
        self.NODEs.vcp_status_led.NODEs.led.PARAMs.color.merge(F.LED.Color.GREEN)
        self.NODEs.vcp_status_led.NODEs.led.PARAMs.brightness.merge(
            TypicalLuminousIntensity.APPLICATION_LED_INDICATOR_INSIDE.value.value
        )

        # connections --------------------------------
        usb.connect(self.NODEs.mcu.IFs.usb)
        uart.connect(self.NODEs.mcu.NODEs.rp2040.IFs.uart)

        # rp2040 swd to programming connector
        mcu_swd.IFs.clk.IFs.signal.connect(self.NODEs.mcu_swd_connector.IFs.unnamed[0])
        gnd.connect(self.NODEs.mcu_swd_connector.IFs.unnamed[1])
        mcu_swd.IFs.dio.IFs.signal.connect(self.NODEs.mcu_swd_connector.IFs.unnamed[2])

        # target swd via level shifters
        # A side is connected to rp2040, B side is connected to target
        # A to B is activated by setting dir to high
        # dio is bidirectional and controlled by the rp2040
        target_swd.IFs.dio.IFs.signal.connect_via(
            self.NODEs.level_shifter[0], self.NODEs.mcu.NODEs.rp2040.IFs.gpio[12]
        )
        self.NODEs.level_shifter[0].IFs.dir.IFs.signal.connect(
            self.NODEs.mcu.NODEs.rp2040.IFs.gpio[1]
        )

        # clk direction is A to B
        target_swd.IFs.clk.IFs.signal.connect_via(
            self.NODEs.level_shifter[1], self.NODEs.mcu.NODEs.rp2040.IFs.gpio[11]
        )
        self.NODEs.level_shifter[1].IFs.dir.IFs.signal.connect(v3_3.IFs.hv)

        # swo direction is B to A
        target_swd.IFs.swo.IFs.signal.connect_via(
            self.NODEs.level_shifter[2], self.NODEs.mcu.NODEs.rp2040.IFs.gpio[14]
        )
        self.NODEs.level_shifter[2].IFs.dir.IFs.signal.connect(gnd)

        # reset direction is A to B
        target_swd.IFs.reset.IFs.signal.connect_via(
            self.NODEs.level_shifter[3], self.NODEs.mcu.NODEs.rp2040.IFs.gpio[15]
        )
        self.NODEs.level_shifter[3].IFs.dir.IFs.signal.connect(v3_3.IFs.hv)

        # specialize

        # set global params
