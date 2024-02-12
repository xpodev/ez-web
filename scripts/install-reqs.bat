@ECHO OFF

%~dp0/../lib/python/python.exe %~dp0/../lib/python/get-pip.py

rem %~dp0/../lib/python/python.exe -m pip install -r %~dp0/reqs.txt

%~dp0/../lib/python/python.exe -m pip install sqlalchemy
%~dp0/../lib/python/python.exe -m pip install argon2-cffi
%~dp0/../lib/python/python.exe -m pip install python-dotenv
%~dp0/../lib/python/python.exe -m pip install fastapi python-socketio uvicorn

%~dp0/../lib/python/python.exe -m pip install jsx --target %~dp0/../core/
