
Dependencies
------------
- python 3
- Python expect - https://github.com/pexpect/pexpect https://pexpect.readthedocs.io/en/stable/ (debian only)
- PS-util  https://psutil.readthedocs.io/en/latest/#windows-services on windows `_pswindows.py` needs to be copied 
 into the python installation after the pip run: 
   - python install root (i.e. Users/willi/AppData/Local/Programs/Python)
   -  /Python38-32/Lib/site-packages/psutil/_pswindows.py
 the upstream distribution doesn't enable the wrappers to start/stop service 
- pyyaml - for parsing saved data.

`pip3 install psutil pyyaml pexpect`

Using
-----

Parameter:
 - `version` which Arangodb Version you want to run the test on
 - `[enterprise|community]` whether its an enterprise or community package you want to install
 - `packageDir` The directory where you downloaded the nsis .exe / deb [/ rpm TODO]
 - `[all|install|uninstall|tests]` (you need to either use `all`, or `install` once and subsequently `tests` until you decide to run `uninstall` to clean your system.

Example usage:
 - Windows: `python3 ./release_tester/test.py 3.6.2 enterprise c:/Users/willi/Downloads all`
 - Linux (ubuntu|debian) `python3 ./release_tester/test.py 3.6.2 enterprise /home/willi/Downloads all`
 - Linux (centos|fedora|sles) TODO


GOAL
====
create most of the flow of i.e. https://github.com/arangodb/release-qa/issues/264 in a portable way. 









Structure going to become:
https://docs.python-guide.org/writing/structure/


attic_snippets/ contains examples and development test code 
