# Installation

## Virtual environments
A very good practice is to use a virtual environment.

A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated Python virtual environments for them.

You may have to install the `venv` package before been able to create a virtual environment, depending on your system. For example, Ubuntu requires `python3-venv` to be installed.

### Create a new venv
```bash
$ python3 -m venv myenv
```

### Activate it
```bash
$ source myenv/bin/activate
(myenv) $
```

## Install Spotipy2
Now install Spotipy2. Since this library isn't on PyPi yet, you can install it only via GitHub.

```bash
(myenv) $ pip install git+https://github.com/CyanBook/spotipy2
```