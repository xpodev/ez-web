@ECHO OFF

set python_path=%~dp0/../lib/python/python.exe

%python_path% %~dp0/../lib/python/get-pip.py

rem %~dp0/../lib/python/python.exe -m pip install -r %~dp0/reqs.txt

%python_path% -m pip install sqlalchemy
%python_path% -m pip install argon2-cffi
%python_path% -m pip install python-dotenv
%python_path% -m pip install fastapi python-socketio uvicorn

%python_path% -m pip install jsx --target %~dp0/../core/

for /d /r %~dp0/../core/ %%f in (*jsx-*) do rmdir /s /q %%f
