# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

"""
This is the entrypoint and boilerplate of the application.
It sets up several paths and calls the app to create the graph.
Afterwards it uses the graph to export to different artifacts (e.g netlist).
"""

import logging
import sys
from pathlib import Path

import faebryk.libs.picker.lcsc as lcsc
import typer
from faebryk.core.module import Module
from faebryk.exporters.esphome.esphome import dump_esphome_config, make_esphome_config
from faebryk.exporters.parameters.parameters_to_file import export_parameters_to_file
from faebryk.exporters.pcb.kicad.artifacts import export_svg
from faebryk.libs.app.checks import run_checks
from faebryk.libs.app.manufacturing import export_pcba_artifacts
from faebryk.libs.app.parameters import replace_tbd_with_any
from faebryk.libs.app.pcb import apply_design
from faebryk.libs.logging import setup_basic_logging
from faebryk.libs.picker.jlcpcb import jlcpcb
from faebryk.libs.picker.jlcpcb.pickers import add_jlcpcb_pickers
from faebryk.libs.picker.picker import pick_part_recursively
from rich.traceback import install
from typing_extensions import Annotated

from rpdap.app import RPDAP
from rpdap.pcb import transform_pcb
from rpdap.pickers import add_app_pickers

# logging settings
logger = logging.getLogger(__name__)


def main(
    export_manufacturing_artifacts: Annotated[
        bool, typer.Option(help="Export manufacturing artifacts (gerbers, BOM, etc.)")
    ] = False,
    export_esphome_config: Annotated[
        bool, typer.Option(help="Export ESPHome config yaml")
    ] = False,
    export_visuals: Annotated[
        bool, typer.Option(help="Export project visuals (e.g. SVG)")
    ] = False,
    export_parameters: Annotated[
        bool, typer.Option(help="Export project parameters to a file")
    ] = False,
):
    # rich traceback settings --------------------------------
    install(width=550, show_locals=True, word_wrap=True)

    # paths --------------------------------------------------
    build_dir = Path("./build")
    faebryk_build_dir = build_dir.joinpath("faebryk")
    faebryk_build_dir.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).parent.parent.parent
    netlist_path = faebryk_build_dir.joinpath("faebryk.net")
    kicad_prj_path = root.joinpath("source")
    pcbfile = kicad_prj_path.joinpath("main.kicad_pcb")
    esphome_path = build_dir.joinpath("esphome")
    esphome_config_path = esphome_path.joinpath("esphome.yaml")
    manufacturing_artifacts_path = build_dir.joinpath("manufacturing")
    parameters_path = faebryk_build_dir.joinpath("parameters.txt")
    visuals_dir = build_dir.joinpath("visuals")

    lcsc.BUILD_FOLDER = build_dir
    lcsc.LIB_FOLDER = root.joinpath("libs")

    # TODO: remove
    jlcpcb.BUILD_FOLDER = Path("./../../faebryk/build")

    # graph --------------------------------------------------
    logger.info("Make app")
    try:
        sys.setrecursionlimit(100000)  # TODO needs optimization
        app = RPDAP()
    except RecursionError:
        logger.error("RECURSION ERROR ABORTING")
        return
    logger.info("Build graph")
    G = app.get_graph()

    run_checks(app, G)

    # fill unspecified parameters ----------------------------
    logger.info("Filling unspecified parameters")
    replace_tbd_with_any(app, recursive=True, loglvl=logging.DEBUG)

    # pick parts ---------------------------------------------
    # from faebryk.libs.picker.picker import logger as picker_logger

    # picker_logger.setLevel(logging.DEBUG)

    logger.info("Picking parts")
    for m in {
        n.get_most_special() for n in app.get_children(direct_only=False, types=Module)
    }:
        add_jlcpcb_pickers(m, base_prio=0)
        add_app_pickers(m)
    pick_part_recursively(app)

    apply_design(pcbfile, netlist_path, G, app, transform_pcb)

    # export visuals -----------------------------------------
    if export_visuals:
        logger.info("Exporting visuals")
        export_svg(pcbfile, visuals_dir.joinpath("pcba.svg"))
    # generate pcba manufacturing and other artifacts ---------
    if export_manufacturing_artifacts:
        export_pcba_artifacts(manufacturing_artifacts_path, pcbfile, app)
        export_svg(pcbfile, manufacturing_artifacts_path.joinpath("pcba.svg"))

    # esphome config -----------------------------------------
    if export_esphome_config:
        logger.info("Generating esphome config")
        esphome_config = make_esphome_config(G)
        esphome_config_path.write_text(
            dump_esphome_config(esphome_config), encoding="utf-8"
        )

    # export all narrowed parameters
    if export_parameters:
        export_parameters_to_file(app, parameters_path)


if __name__ == "__main__":
    setup_basic_logging()
    typer.run(main)
