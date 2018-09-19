"""
This is a rather klunky solution to the problem of how to use different settings files on different servers.
Uncomment the appropriate line according to which machine is being used.
On the development machine, use dev.py, on the production machine, use prod.py
"""

from .dev import *

# from .prod import *