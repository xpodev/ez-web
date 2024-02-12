# TODO: Remove this code because PYTHONPATH should work
import sys
import os

for path in os.environ["EZ_PYTHONPATH"].split(os.pathsep):
    sys.path.append(path)

import ez

app = ez._app

if __name__ == "__main__":
    ez.run()
