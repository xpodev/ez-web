py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r reqs.txt
echo "import os;import sys;sys.path.insert(0, os.environ['VIRTUAL_ENV'].replace(os.sep + '.venv', '') + os.sep + 'src')" | Out-File -FilePath .venv\Lib\site-packages\dev.pth -Encoding ascii
uvicorn src.main:Ez.app --reload