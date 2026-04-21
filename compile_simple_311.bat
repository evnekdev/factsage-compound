REM compile.bat

REM python setup.py build_ext --inplace

..\venv-setup_3.11_x64\Scripts\python.exe -m pip install --upgrade pip
..\venv-setup_3.11_x64\Scripts\pip.exe install setuptools
..\venv-setup_3.11_x64\Scripts\pip.exe install cython
..\venv-setup_3.11_x64\Scripts\pip.exe install wheel
..\venv-setup_3.11_x64\Scripts\python.exe setup.py bdist_wheel

