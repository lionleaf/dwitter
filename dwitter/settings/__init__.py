from dwitter.settings.base import *


try:
      from dwitter.settings.local import *
except ImportError:
        raise ImportError("Failed to import local settings")
