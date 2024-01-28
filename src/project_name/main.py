# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

"""
This is the entrypoint and boilerplate of the application.
It sets up several paths and calls the app to create the graph.
Afterwards it uses the graph to export to different artifacts (e.g netlist).
"""

import logging
from pathlib import Path

import typer
from faebryk.libs.app.kicad_netlist import write_netlist
from faebryk.libs.logging import setup_basic_logging
from project_name.app import MyApp

# from project_name.pcb import transform_pcb
# from faebryk.exporters.pcb.kicad.transformer import PCB_Transformer
# from faebryk.exporters.visualize.graph import render_matrix
# from faebryk.libs.kicad.pcb import PCB

logger = logging.getLogger(__name__)


def main():
    # paths --------------------------------------------------
    build_dir = Path("./build")
    faebryk_build_dir = build_dir.joinpath("faebryk")
    faebryk_build_dir.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).parent.parent.parent
    kicad_prj_path = root.joinpath("source")
    netlist_path = kicad_prj_path.joinpath("main.net")
    # pcbfile = kicad_prj_path.joinpath("main.kicad_pcb")

    import faebryk.libs.picker.lcsc as lcsc

    lcsc.BUILD_FOLDER = build_dir
    lcsc.LIB_FOLDER = root / "libs"

    # graph --------------------------------------------------
    app = MyApp()
    G = app.get_graph()

    # visualize ----------------------------------------------
    # render_matrix(
    #     G.G,
    #     nodes_rows=[],
    #     depth=1,
    #     show_full=True,
    #     show_non_sum=False,
    # ).show()

    # netlist -----------------------------------------------
    write_netlist(G, netlist_path, use_kicad_designators=True)

    # pcb ----------------------------------------------------
    # logger.info("Load PCB")
    # pcb = PCB.load(pcbfile)

    # transformer = PCB_Transformer(pcb, G, app)

    # logger.info("Transform PCB")
    # transform_pcb(transformer)

    # logger.info(f"Writing pcbfile {pcbfile}")
    # pcb.dump(pcbfile)
    # ---------------------------------------------------------


if __name__ == "__main__":
    setup_basic_logging()
    typer.run(main)
