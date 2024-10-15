# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.picker.lcsc import LCSC_Part
from faebryk.libs.picker.picker import PickerOption, pick_module_by_params
from faebryk.libs.units import P

logger = logging.getLogger(__name__)

"""
This file is for picking actual electronic components for your design.
You can make use of faebryk's picker & parameter system to do this.
"""


# part pickers --------------------------------------------
def pick_capacitor(module: F.Capacitor):
    """
    Link a partnumber/footprint to a Capacitor

    Uses 0402 when possible
    """

    pick_module_by_params(
        module,
        [
            PickerOption(
                part=LCSC_Part(partno="C1525"),
                params={
                    "temperature_coefficient": F.Constant(
                        F.Capacitor.TemperatureCoefficient.X7R,
                    ),
                    "capacitance": F.Constant(100 * P.nF),
                    "rated_voltage": F.Constant(16 * P.V),
                },
            ),
            PickerOption(
                part=LCSC_Part(partno="C19702"),
                params={
                    "temperature_coefficient": F.Constant(
                        F.Capacitor.TemperatureCoefficient.X7R,
                    ),
                    "capacitance": F.Constant(10 * P.uF),
                    "rated_voltage": F.Constant(10 * P.V),
                },
            ),
            PickerOption(
                part=LCSC_Part(partno="C25076"),
                params={
                    "temperature_coefficient": F.Constant(
                        F.Capacitor.TemperatureCoefficient.X5R,
                    ),
                    "capacitance": F.Constant(10 * P.uF),
                    "rated_voltage": F.Constant(25 * P.V),
                },
            ),
        ],
    )


def pick_led(module: F.LED):
    pick_module_by_params(
        module,
        [
            # TODO: use parameters to select the right part?
            # PickerOption(
            #    part=LCSC_Part(partno="C2286"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.GREEN),
            #        "max_brightness": F.Constant(285e-3),
            #        "forward_voltage": F.Constant(3.7),
            #        "max_current": F.Constant(100e-3),
            #    },
            #    pinmap={"1": module.cathode, "2": module.anode},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C72041"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.BLUE),
            #        "max_brightness": F.Constant(28.5e-3),
            #        "forward_voltage": F.Constant(3.1),
            #        "max_current": F.Constant(100e-3),
            #    },
            #    pinmap={"1": module.cathode, "2": module.anode},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C2290"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.WHITE),
            #        "max_brightness": F.Constant(520e-3),
            #        "forward_voltage": F.Constant(3.1),
            #        "max_current": F.Constant(60e-3),
            #    },
            #    pinmap={"2": module.cathode, "1": module.anode},
            # ),
            # PickerOption(
            #    part=LCSC_Part(partno="C2296"),
            #    params={
            #        "color": F.Constant(TypicalColorsByWavelength.YELLOW),
            #        "max_brightness": F.Constant(113e-3),
            #        "forward_voltage": F.Constant(2.1),
            #        "max_current": F.Constant(20e-3),
            #    },
            #    pinmap={"2": module.cathode, "1": module.anode},
            # ),
            # MHT151WDT
            PickerOption(
                part=LCSC_Part(partno="C401114"),
                params={
                    "color": F.Constant(F.LED.Color.YELLOW),
                    "max_brightness": F.Constant(900 * P.millicandela),
                    "forward_voltage": F.Constant(3.15 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # MHT151UGCT
            PickerOption(
                part=LCSC_Part(partno="C559120"),
                params={
                    "color": F.Constant(F.LED.Color.GREEN),
                    "max_brightness": F.Constant(1120 * P.millicandela),
                    "forward_voltage": F.Constant(3.05 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # XL-1606SURC
            PickerOption(
                part=LCSC_Part(partno="C965860"),
                params={
                    "color": F.Constant(F.LED.Color.RED),
                    "max_brightness": F.Constant(220 * P.millicandela),
                    "forward_voltage": F.Constant(2.4 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # XL-1606SYGC
            # PickerOption(
            #    part=LCSC_Part(partno="C965864"),
            #    params={
            #        "color": F.Constant(F.LED.Color.YELLOW),
            #        "max_brightness": F.Constant(130 * P.millicandela),
            #        "forward_voltage": F.Constant(2.4 * P.V),
            #        "max_current": F.Constant(20 * P.mA),
            #    },
            #    pinmap={"1": module.cathode, "2": module.anode},
            # ),
            # XL-1606UBC
            PickerOption(
                part=LCSC_Part(partno="C965865"),
                params={
                    "color": F.Constant(F.LED.Color.BLUE),
                    "max_brightness": F.Constant(260 * P.millicandela),
                    "forward_voltage": F.Constant(2.4 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # XL-1606UGC
            # PickerOption(
            #    part=LCSC_Part(partno="C965863"),
            #    params={
            #        "color": F.Constant(F.LED.Color.GREEN),
            #        "max_brightness": F.Constant(1100 * P.millicandela),
            #        "forward_voltage": F.Constant(3.4 * P.V),
            #        "max_current": F.Constant(20 * P.mA),
            #    },
            #    pinmap={"1": module.cathode, "2": module.anode},
            # ),
            # XL-1606UOC
            PickerOption(
                part=LCSC_Part(partno="C965861"),
                params={
                    "color": F.Constant(F.LED.Color.ORANGE),
                    "max_brightness": F.Constant(230 * P.millicandela),
                    "forward_voltage": F.Constant(2.4 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
            # XL-1606UWC
            PickerOption(
                part=LCSC_Part(partno="C965866"),
                params={
                    "color": F.Constant(
                        F.LED.Color.WARM_WHITE
                        # TypicalColorByTemperature.WARM_WHITE_FLUORESCENT_LED
                    ),
                    "max_brightness": F.Constant(1100 * P.millicandela),
                    "forward_voltage": F.Constant(3.4 * P.V),
                    "max_current": F.Constant(20 * P.mA),
                },
                pinmap={"1": module.cathode, "2": module.anode},
            ),
        ],
    )


# ----------------------------------------------------------


def add_app_pickers(module: Module):
    lookup = {
        F.LED: pick_led,
        F.Capacitor: pick_capacitor,
    }

    F.has_multi_picker.add_pickers_by_type(
        module,
        lookup,
        F.has_multi_picker.FunctionPicker,
    )
