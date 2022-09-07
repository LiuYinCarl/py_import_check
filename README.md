# py\_import\_check

In Python Project, hotfix is very frequent, but some bad habits in write  
Python Code will cause hotfix failed, for example.

```python
# a.py

CONST_VAL = 100 # an integer value
```

```python
# b.py

from a import CONST_VAL

def func():
	print(CONST_VAL)
```

if we hotfix `a.py` and change it's content to below.

```python
# a.py

CONST_VAL = 200 # an integer value
```

in `a.py`, `CONST_VAL` will be 200, but in `b.py`, the `CONST_VAL` is still 100.

So, we need find out all invalid import in a project and it's the purpose of  
the project.

