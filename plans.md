> [!NOTE]
> These are all just mere ideas for myself and may not make the final cut in production.
# Redesign Heavy Backend Functions in C
Since there is going to be some very IO (input/output) heavy tasks, it could be benificial
to have them written in C as a **shared object** file. These functions I find don't change
or even really need to be changed very often, so just letting them live in libraries and
mostly only passing them data from the more front-end of things would be a nice
abstraction, letting me think about the bigger picture of the project.

This can be done by using Python's standard library `ctypes`. I.e.:
```python
# file: main.py

import ctypes

libc = ctypes.CDLL("lib.so") # Load the library

number = libc.add(5, 5) # Call the library function

print(f"From C: {number}") # Use the return value of the function like any other variable in Python.
```

Output:
```
> python main.py
From C: 10
```

Wrappers for these functions will be made for further Python integration, like passing
function paramaters via keyword arguments and type hints.

# Install Design
The idea for how the binary executable, shared libraries, configuration data, ect. will be
installed is by installing to a self-contained environment within `/opt`. This is what I think
is the best course of action as making packages for a bunch of distros would be tedious, just
so for the install target to be in `/usr`, unless I got a few people to help with packaging for
each new release.

Outside of `/opt`, a .service file would be installed for `systemd` at `/etc/systemd/system`
and maybe a symlink in `$PATH` to the executable that'll most likely be in `/opt/bin`.

This design could easily change if there would be a better design and/or better complince
with the FHS 3.0.
