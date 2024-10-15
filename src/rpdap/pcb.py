# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging
import subprocess

import faebryk.library._F as F
from faebryk.exporters.pcb.kicad.transformer import (
    Alignment,
    Font,
    PCB_Transformer,
    Point2D,
)
from faebryk.exporters.pcb.layout.absolute import LayoutAbsolute
from faebryk.exporters.pcb.layout.extrude import LayoutExtrude
from faebryk.exporters.pcb.layout.heuristic_decoupling import (
    LayoutHeuristicElectricalClosenessDecouplingCaps,
    Params,
)
from faebryk.exporters.pcb.layout.heuristic_pulls import (
    LayoutHeuristicElectricalClosenessPullResistors,
)
from faebryk.exporters.pcb.layout.typehierarchy import LayoutTypeHierarchy
from faebryk.libs.geometry.basic import Geometry
from faebryk.libs.kicad.fileformats import C_fp_text, C_text_layer
from faebryk.libs.kicad.fileformats_common import C_effects, C_wh, C_xy, C_xyr

from rpdap.app import RPDAP
from rpdap.modules.faebrykLogo import faebrykLogo
from rpdap.modules.RPDAPModule import RPDAPModule

logger = logging.getLogger(__name__)

"""
Here you can do PCB scripting.
E.g placing components, layer switching, mass renaming, etc.
"""


# ----------------------------------------
#               Functions
# ----------------------------------------
def apply_routing(transformer: PCB_Transformer):
    pass


def add_zone(transformer: PCB_Transformer, outline: list[Point2D], offset: float = 1):
    transformer.insert_zone(
        net=transformer.get_net(F.Net.with_name("GND")),
        layers=[*transformer.get_copper_layers()],
        polygon=Geometry.rect_to_polygon(
            Geometry.bbox(
                [Geometry.Point2D(coord) for coord in outline],
                offset,
            )
        ),
    )


def add_graphical_elements(
    transformer: PCB_Transformer, board_size: tuple[float, float]
):
    app = transformer.app
    assert isinstance(app, RPDAP)

    board_width, board_height = board_size

    # project name and version
    board_name = "RPDAP"
    char_size = board_width / (len(board_name) - 1)
    transformer.insert_text(
        text=board_name,
        at=C_xyr(6, board_height / 2, 90),
        layer="B.SilkS",
        font=Font(size=C_wh(char_size, char_size), thickness=0.6),
        knockout=True,
    )
    try:
        git_human_version = (
            subprocess.check_output(["git", "describe", "--always"])
            .strip()
            .decode("utf-8")
        )
    except subprocess.CalledProcessError:
        logger.warning("Cannot get git project version")
        git_human_version = "Cannot get git project version"

    transformer.insert_text(
        text=git_human_version,
        at=C_xyr(11, board_height / 2, 90),
        layer="B.SilkS",
        font=Font(size=C_wh(1, 1), thickness=0.15),
        knockout=True,
    )

    # LED text
    led_font = Font(size=C_wh(1.75, 1.75), thickness=0.25)
    transformer.insert_text(
        text="[ ] VCP ",
        at=C_xyr(13.38, 13.5, 90),
        layer="B.SilkS",
        font=led_font,
        knockout=True,
        alignment=Alignment(
            (
                C_effects.C_justify.E_justify.left,
                C_effects.C_justify.E_justify.center_vertical,
                C_effects.C_justify.E_justify.mirror,
            )
        ),
    )
    transformer.insert_text(
        text="[ ] DAP ",
        at=C_xyr(16.63, 13.5, 90),
        layer="B.SilkS",
        font=led_font,
        knockout=True,
        alignment=Alignment(
            (
                C_effects.C_justify.E_justify.left,
                C_effects.C_justify.E_justify.center_vertical,
                C_effects.C_justify.E_justify.mirror,
            )
        ),
    )

    # JLCPCB QR code
    transformer.insert_jlcpcb_qr(
        transformer.JLCPBC_QR_Size.MEDIUM_8x8mm,
        center_at=C_xy(15, 33),
        layer="B.SilkS",
        number=True,
    )

    # move all reference designators to the same position
    transformer.set_designator_position(
        offset=0.75,
        displacement=C_xy(0, 0),
        offset_side=PCB_Transformer.Side.BOTTOM,
        layer=None,
        font=Font(size=C_wh(0.5, 0.5), thickness=0.1),
        knockout=None,
    )


def add_marking(transformer: PCB_Transformer):
    for fp in transformer.pcb.footprints:
        if not any(
            [
                x.text == "FBRK:autoplaced" or x.text == "FBRK:notouch"
                for x in fp.fp_texts
            ]
        ):
            fp.fp_texts.append(
                C_fp_text(
                    type=C_fp_text.E_type.user,
                    text="FBRK:not_autoplaced",
                    at=C_xyr(0, 0, fp.at.r),
                    effects=C_effects(transformer.font),
                    uuid=transformer.gen_uuid(mark=True),
                    layer=C_text_layer("User.5"),
                )
            )


def apply_root_layout(app: RPDAP, board_size: tuple[float, float]):
    Point = F.has_pcb_position.Point
    L = F.has_pcb_position.layer_type
    LVL = LayoutTypeHierarchy.Level

    board_width, board_height = board_size

    LayoutHeuristicElectricalClosenessDecouplingCaps.add_to_all_suitable_modules(
        app,
        params=Params(
            distance_between_pad_edges=0.5,
        ),
    )
    LayoutHeuristicElectricalClosenessPullResistors.add_to_all_suitable_modules(
        app,
        params=Params(
            distance_between_pad_edges=0.5,
        ),
    )

    for led_indicator in app.get_children_modules(types=F.LEDIndicator):
        led_indicator.add_trait(
            F.has_pcb_layout_defined(
                LayoutTypeHierarchy(
                    layouts=[
                        LVL(
                            mod_type=F.LED,
                            layout=LayoutAbsolute(Point((0, 0, 0, L.NONE))),
                        ),
                        LVL(
                            mod_type=F.Resistor,
                            layout=LayoutAbsolute(Point((-4.5, 0, 180, L.NONE))),
                        ),
                    ]
                ),
            )
        )

    # manual placement
    layouts = [
        LVL(
            mod_type=RPDAPModule,
            layout=LayoutAbsolute(Point((board_width / 2, 0, 0, L.TOP_LAYER))),
        ),
        LVL(
            mod_type=faebrykLogo,
            layout=LayoutAbsolute(Point((6, 8, 90, L.BOTTOM_LAYER))),
        ),
        LVL(
            mod_type=F.RaspberryPiPicoBase_ReferenceDesign,
            layout=LayoutAbsolute(Point((8, board_height / 2 - 0.5, 0, L.TOP_LAYER))),
            children_layout=LayoutTypeHierarchy(
                layouts=[
                    LVL(
                        mod_type=F.LEDIndicator,
                        layout=LayoutAbsolute(Point((8.75, -14.5, 90, L.NONE))),
                    ),
                ]
            ),
        ),
        LVL(
            mod_type=F.Wuxi_I_core_Elec_AiP74LVC1T45GB236_TR,
            layout=LayoutExtrude(
                base=Point((2, board_height - 10, 0, L.TOP_LAYER)),
                vector=(3.25, 0, 0),
            ),
        ),
        LVL(
            mod_type=F.LEDIndicator,
            layout=LayoutAbsolute(Point((13.5, 10, 90, L.TOP_LAYER))),
        ),
    ]

    app.add_trait(F.has_pcb_layout_defined(LayoutTypeHierarchy(layouts)))

    # set coordinate system
    app.add_trait(F.has_pcb_position_defined(Point((0, 0, 0, L.NONE))))


def transform_pcb(transformer: PCB_Transformer):
    app = transformer.app
    assert isinstance(app, RPDAP)

    # ----------------------------------------
    #               PCB outline
    # ----------------------------------------
    board_width = 20
    board_height = 50
    outline_coordinates = [
        (0, 0),
        (board_width, 0),
        (board_width, board_height),
        (0, board_height),
    ]

    transformer.set_pcb_outline_complex(
        geometry=transformer.create_rectangular_edgecut(
            width_mm=board_width,
            height_mm=board_height,
            # rounded_corners=True, #TODO: fix this
            # corner_radius_mm=2.5,
            origin=(0, 0),
        ),
        remove_existing_outline=True,
        # corner_radius_mm=2.5,
    )

    # ----------------------------------------
    #               Copper zones
    # ----------------------------------------
    add_zone(transformer, outline_coordinates, offset=1)

    # ----------------------------------------
    #               Layout
    # ----------------------------------------
    apply_root_layout(app, board_size=(board_width, board_height))

    # ----------------------------------------
    #               Routing
    # ----------------------------------------
    apply_routing(transformer)

    # ----------------------------------------
    #           Graphical elements
    # ----------------------------------------
    add_graphical_elements(transformer, board_size=(board_width, board_height))
    add_marking(transformer)
