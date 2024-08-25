# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.core import Module

logger = logging.getLogger(__name__)


class faebrykLogo(Module):
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
            pass

        return _IFS

    def __init__(self):
        # boilerplate
        super().__init__()
        self.IFs = self.IFS()(self)
        self.PARAMs = self.PARAMS()(self)
        self.NODEs = self.NODES()(self)

        # connections

        # traits
        self.add_trait(F.has_designator_prefix_defined("LOGO"))

        self.add_trait(F.can_attach_to_footprint_via_pinmap(pinmap={})).attach(
            F.KicadFootprint("custom:faebryk_logo", pin_names=[])
        )
