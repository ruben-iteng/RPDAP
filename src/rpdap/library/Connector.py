# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

from faebryk.core.core import Module
from faebryk.library.Electrical import Electrical
from faebryk.libs.util import times

logger = logging.getLogger(__name__)


class Connector(Module):
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
            unnamed = times(3, Electrical)

        return _IFS

    def __init__(self):
        # boilerplate
        super().__init__()
        self.IFs = self.IFS()(self)
        self.PARAMs = self.PARAMS()(self)
        self.NODEs = self.NODES()(self)

        # connections

        # traits
