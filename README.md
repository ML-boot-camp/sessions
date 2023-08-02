# sessions

This the GitHub repository of the course.

To access the course material go there: https://ml-boot-camp.github.io/sessions/

## Installation

Python management is done with mamba (see [installation instructions here](https://mamba.readthedocs.io/en/latest/installation.html)) and relies on the [conda-forge](https://conda-forge.org/) packages.

So we recommend to use [mambaforge](https://github.com/conda-forge/miniforge#mambaforge). To install on OSX, simply run in a terminal:
```shell
brew install mambaforge
```

### Install the project dependencies

Create the environment:
```shell
mamba env create -f environment.yml
```

Activate it:
```shell
mamba activate ml-bootcamp
```

## Update content

### Notebooks
After updating the python scripts:
```shell
cd notebooks
make
```

### Markdown

To display your updates in a dev server:
```shell
mkdocs serve
```
