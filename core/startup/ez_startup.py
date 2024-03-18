from pathlib import Path

import args


__version__ = "0.1.0"


#region EZ Framework Initialization


import ez

ez.EZ_FRAMEWORK_DIR = Path(__file__).parent.parent.parent
ez.EZ_FRAMEWORK_VERSION = __version__
ez.EZ_PYTHON_EXECUTABLE = str(ez.EZ_FRAMEWORK_DIR / "lib" / "python" / "python.exe")

ez.SITE_DIR = args.args.sitedir


#endregion


