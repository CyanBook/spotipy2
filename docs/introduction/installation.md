# Installation
Being a modern Python framework, Spotipy2 requires an up-to-date version of Python to be installed in your system. We recommend using the latest versions of both Python 3 and pip.


## Install Spotipy2
The easiest way to install the latest stable version of Spotipy2 is via **pip**
```bash
pip install spotipy2
```

If you want to enable caching:
```bash
pip install spotipy2[cache]
```

If you want the last development build:
```bash
pip install git+https://github.com/CyanBook/spotipy2
```

### Verifying
To be sure that Spotipy2 has been correctly downloaded and installed, try to open a Python shell and import it.
```python
>>> import spotipy2
>>> spotipy2.__version__
'x.y.z'
```

## Virtual environments
A very good practice is to use a virtual environment.

A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated Python virtual environments for them.

You may have to install the `venv` package before been able to create a virtual environment, depending on your system. For example, Ubuntu requires `python3-venv` to be installed.

### Create and activate one
```bash
$ python3 -m venv .env
$ source .env/bin/activate
(.env) $ python -c "import sys; print(sys.executable)" # Check if it's working
.../.env/bin/python
```