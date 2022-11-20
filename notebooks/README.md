# notebooks

## Installation

Virtualenv management is done with:

- pyenv
- pip-tools

### Install pyenv

Install pyenv:
```
curl https://pyenv.run | bash
```

> Note: You may need to update `.bashrc` or `.zshrc` and restart your shell. 

Install [pyenv required dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) to compile and install python:

- Ubuntu:
    ```
    sudo apt update; sudo apt install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
    ```
- OSX:
    ```
    brew install openssl readline sqlite3 xz zlib tcl-tk
    ```

### Create virtual environment

Install a recent python version:
```
pyenv install 3.10.8
```

> Note: If needed, please refer to [pyenv's common build problems doc](https://github.com/pyenv/pyenv/wiki/Common-build-problems).

Create a virtualenv named `ml-boot-camp`:
```
pyenv virtualenv 3.10.8 ml-boot-camp
```

### Install pip-tools & the project dependencies

Activate the environment:
```
pyenv activate ml-boot-camp
```

Install pip-tools:
```
pip install pip-tools
```

Compile the `requirements.txt`, if this hasn't been done already:
```
pip-compile requirements.in
```

> Note: if `requirements.txt` exists already, it won't be overwritten. If you wish to recompile the dependencies, you need to delete first the `requirements.txt` file.

Install the dependencies:
```
pip-sync requirements.txt
```

## To modify the notebooks

- Update or create a **python script in the `src` directory**: e.g `src/1_data_engineering.py`
- In the script, add markers containing `LINE TO BE REMOVED FOR STUDENTS`
- Then run the makefile:
  ```make```

Then the students' version for the script and all the notebooks will be generated automatically **in the `build` directory**.
