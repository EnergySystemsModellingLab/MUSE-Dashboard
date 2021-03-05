# Bugs in MUSE

README contains installation errors:
 - Egg info is incorrect and fails to install: `python -m pip install git+https://github.com/SGIModel/StarMuse.git#egg=muse` should be:
 ```
 python -m pip install git+https://github.com/SGIModel/StarMuse.git#egg=StarMUSE
 ```

Cannot load MCA:
 - `MCA.factory()` fails because `mypy_extensions` is a requirement but not installed in the setup
 ```
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
   File "/Users/adalessa/Projects/MUSE/muse-dashboard/.venv/lib/python3.8/site-packages/muse/mca.py", line 44, in factory
     from muse.outputs.mca import factory as ofactory
   File "/Users/adalessa/Projects/MUSE/muse-dashboard/.venv/lib/python3.8/site-packages/muse/outputs/__init__.py", line 2, in <module>
     from muse.outputs import sector, sinks
   File "/Users/adalessa/Projects/MUSE/muse-dashboard/.venv/lib/python3.8/site-packages/muse/outputs/sector.py", line 26, in <module>
     from mypy_extensions import KwArg
 ModuleNotFoundError: No module named 'mypy_extensions'
```
