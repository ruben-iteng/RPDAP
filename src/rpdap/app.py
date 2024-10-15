# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging
from math import inf

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.brightness import TypicalLuminousIntensity
from faebryk.libs.library import L
from faebryk.libs.units import P

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


class RPDAP(Module):
    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    rpdap_module: RPDAPModule
    faebryk_logo: faebrykLogo
    mcu: F.RaspberryPiPicoBase_ReferenceDesign
    vcp_status_led = L.f_field(F.LEDIndicator)(use_mosfet=False)
    level_shifter = L.list_field(6, F.Wuxi_I_core_Elec_AiP74LVC1T45GB236_TR)
    gnd_detect_current_limit: F.Resistor

    def __preinit__(self):
        # ----------------------------------------
        #                aliasess
        # ----------------------------------------
        vbus = self.rpdap_module.usb.usb_if.buspower
        gnd = vbus.lv
        v3_3 = self.mcu.ldo.power_out
        usb = self.rpdap_module.usb
        target_swd = self.rpdap_module.swd
        target_uart = self.rpdap_module.uart

        # ----------------------------------------
        #                net names
        # ----------------------------------------
        nets = {
            "VBUS": vbus.hv,
            "3V3": v3_3.hv,
            "VTARGET": self.rpdap_module.device_power.hv,
            "GND": gnd,
            "USB_P": usb.usb_if.d.p.signal,
            "USB_N": usb.usb_if.d.n.signal,
            "SWD_CLK": target_swd.clk.signal,
            "SWD_DIO": target_swd.dio.signal,
            "SWD_SWO": target_swd.swo.signal,
            "SWD_RESET": target_swd.reset.signal,
            "GND_DETECT": self.rpdap_module.gnd_detect.signal,
            "UART_RX": target_uart.rx.signal,
            "UART_TX": target_uart.tx.signal,
        }
        for net_name, mif in nets.items():
            assert isinstance(
                mif, F.Electrical
            ), f"You are trying to give a non-electrical interface: {mif}, a net name: {net_name}"  # noqa E501
            net = F.Net.with_name(net_name)
            net.part_of.connect(mif)

        # ----------------------------------------
        #            parametrization
        # ----------------------------------------
        self.vcp_status_led.led.led.color.merge(F.LED.Color.GREEN)
        self.vcp_status_led.led.led.brightness.merge(
            TypicalLuminousIntensity.APPLICATION_LED_INDICATOR_INSIDE.value.value
        )
        self.gnd_detect_current_limit.resistance.merge(
            F.Range.from_center_rel(100 * P.ohm, 0.01)
        )

        # ----------------------------------------
        #              connections
        # ----------------------------------------
        # usb
        usb.connect(self.mcu.usb)

        # vcp (virtual com port) status led
        self.mcu.rp2040.gpio[2].connect(self.vcp_status_led.logic_in)

        # GND detect (pull-up by default)
        self.mcu.rp2040.gpio[3].signal.connect_via(
            self.gnd_detect_current_limit, self.rpdap_module.gnd_detect.signal
        )
        self.mcu.rp2040.gpio[3].set_weak(on=True)

        # target swd via level shifters
        # A side is connected to rp2040, B side is connected to target
        # A to B is activated by setting dir to high
        # dio is bidirectional and controlled by the rp2040
        self.mcu.rp2040.gpio[12].connect_via(self.level_shifter[0], target_swd.dio)
        self.level_shifter[0].direction.connect(self.mcu.rp2040.gpio[9])

        # clk direction is A to B
        self.mcu.rp2040.gpio[11].connect_via(self.level_shifter[1], target_swd.clk)
        self.level_shifter[1].direction.set_weak(on=True)

        # swo direction is B to A
        self.mcu.rp2040.gpio[14].connect_via(self.level_shifter[2], target_swd.swo)
        self.level_shifter[2].direction.set_weak(on=False)

        # reset direction is A to B
        self.mcu.rp2040.gpio[15].connect_via(self.level_shifter[3], target_swd.reset)
        self.level_shifter[3].direction.set_weak(on=True)

        # uart via level shifter
        self.mcu.rp2040.uart[0].base_uart.tx.connect_via(
            self.level_shifter[4], target_uart.tx
        )
        self.level_shifter[4].direction.set_weak(on=False)
        self.mcu.rp2040.uart[0].base_uart.rx.connect_via(
            self.level_shifter[5], target_uart.rx
        )
        self.level_shifter[5].direction.set_weak(on=True)

        # level shifter power
        for shifter in self.level_shifter:
            shifter.power_a.connect(v3_3)
            shifter.power_b.connect(self.rpdap_module.device_power)
            shifter.direction.reference.connect(v3_3)

        # ----------------------------------------
        #              specialization
        # ----------------------------------------

        # ----------------------------------------
        # set global params
        # ----------------------------------------
        # TODO: remove
        for reference in [
            self.mcu.adc_voltage_reference.rc_filter.in_.reference,
            self.mcu.adc_voltage_reference.rc_filter.out.reference,
        ]:
            reference.voltage.merge(F.Constant(3.3 * P.V))

        for res in self.get_children_modules(types=F.Resistor, include_root=True):
            resistance = res.resistance
            if isinstance(resistance.get_most_narrow(), (F.TBD, F.ANY)):
                resistance.merge(F.Range.from_center_rel(10 * P.kohm, 0.05))

        for cap in self.get_children_modules(types=F.Capacitor, include_root=True):
            capacitance = cap.capacitance
            temperature_coefficient = cap.temperature_coefficient
            rated_voltage = cap.rated_voltage
            if isinstance(capacitance.get_most_narrow(), (F.TBD, F.ANY)):
                capacitance.merge(F.Range.from_center(100 * P.nF, 1 * P.nF))
            if isinstance(temperature_coefficient.get_most_narrow(), (F.TBD, F.ANY)):
                temperature_coefficient.merge(
                    F.Range(
                        F.Capacitor.TemperatureCoefficient.Y5V,
                        F.Capacitor.TemperatureCoefficient.C0G,
                    )
                )
            if isinstance(rated_voltage.get_most_narrow(), (F.TBD, F.ANY)):
                rated_voltage.merge(F.Range(10 * P.V, inf * P.V))  # TODO: dangerous
