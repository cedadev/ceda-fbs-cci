from .src.fbs import (
    cmdline,
    es_iface,
    proc
)

import pkg_resources
__version__ = pkg_resources.get_distribution('ceda-fbs').version