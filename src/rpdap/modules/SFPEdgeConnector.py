# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

from faebryk.core.core import Module
from faebryk.library.can_attach_to_footprint_via_pinmap import (
    can_attach_to_footprint_via_pinmap,
)
from faebryk.library.Electrical import Electrical
from faebryk.library.has_designator_prefix_defined import has_designator_prefix_defined
from faebryk.library.KicadFootprint import KicadFootprint
from faebryk.libs.util import times

logger = logging.getLogger(__name__)


class SFPEdgeConnector(Module):
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
            unnamed = times(20, Electrical)

        return _IFS

    def __init__(self):
        # boilerplate
        super().__init__()
        self.IFs = self.IFS()(self)
        self.PARAMs = self.PARAMS()(self)
        self.NODEs = self.NODES()(self)

        # connections

        # traits
        self.add_trait(has_designator_prefix_defined("J"))

        self.add_trait(
            can_attach_to_footprint_via_pinmap(
                pinmap={f"{i+1}": self.IFs.unnamed[i] for i in range(20)}
            )
        ).attach(
            KicadFootprint("custom:SFP_Edge", pin_names=[f"{i+1}" for i in range(20)])
        )
