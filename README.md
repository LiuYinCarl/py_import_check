# py\_import\_check

## Introduce

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

So, we need find out all invalid import in a project and it's the purpose of the project.

## Usage

django is a big enough open source project to test our code, so I write a shell script to 
test it. You can run the test using command `sh django_test.sh`.

Then, it will download the django project and auto run test, the output will both output to 
Terminal and `django.log`.

If you want to test your project, just edit `config.py` and set `TEST_DJANGO = False`, then 
run `python3 main.py`.