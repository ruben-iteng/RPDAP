# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

"""
TODO: Explain file
"""

from pathlib import Path
import logging

logger = logging.getLogger("main")


# function imports
from faebryk.exporters.netlist.kicad.netlist_kicad import (
    from_faebryk_t2_netlist,
)
from faebryk.exporters.netlist.netlist import make_t2_netlist_from_t1
from faebryk.exporters.netlist.graph import (
    make_graph_from_components,
    make_t1_netlist_from_graph,
)

# library imports
from faebryk.library.core import Component, Interface
from faebryk.library.library.components import (
    Resistor,
    Capacitor,
)
from faebryk.library.library.interfaces import Power, Electrical
from faebryk.library.library.parameters import Constant, TBD
from faebryk.library.library.footprints import SMDTwoPin
from faebryk.library.traits.component import has_footprint
from faebryk.library.trait_impl.component import (
    has_symmetric_footprint_pinmap,
    has_defined_footprint,
    can_bridge_defined,
    has_defined_footprint_pinmap,
)

# Project library imports
#from library.library.components import ()

K = 1000
M = 1000_000
G = 1000_000_000

n = 0.001 * 0.001 * 0.001
u = 0.001 * 0.001




class Project(Component):
    def __init__(self) -> None:
        super().__init__()

        # interfaces
        class _IFs(Component.InterfacesCls()):
            pass
        self.IFs = _IFs(self)

        # components
        class _CMPs(Component.ComponentsCls()):
            pass
        self.CMPs = _CMPs(self)

        # power

        # function

        # hack footprints
        for r in self.CMPs.get_all():
            if not r.has_trait(has_footprint):
                r.add_trait(has_symmetric_footprint_pinmap())

        self.add_trait(has_symmetric_footprint_pinmap())


G = Project()
CMPs = [G]


t1_ = make_t1_netlist_from_graph(make_graph_from_components(CMPs))
netlist = from_faebryk_t2_netlist(make_t2_netlist_from_t1(t1_))

Path("./build/faebryk/").mkdir(parents=True, exist_ok=True)
path = Path("./build/faebryk/faebryk.net")
logger.info("Writing Experiment netlist to {}".format(path.resolve()))
path.write_text(netlist, encoding="utf-8")

from faebryk.exporters.netlist.netlist import render_graph

render_graph(t1_)
