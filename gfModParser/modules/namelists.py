# SPDX-License-Identifier: GPL-2.0+

from . import procedures


# Reuse arglist as it's just a list of symbol references of each component
# of the namelist
class namelist(procedures.arglist):
    pass
