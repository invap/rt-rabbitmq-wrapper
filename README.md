# Implementation of The Runtime RabbitMQ wrapper for The Runtime Monitor tool constellation

This little project implements a wrapper containing functions and classes used in the implementation of the different components of The Runtime Monitor tool constellation. It provides that means for communicating via RabbitMQ servers. The code contained in the project is not meant to be used by its own as it is tailored to the needs of such components.


## Setting up the project using Poetry
This section provide instructions for setting up the project using [Poetry](https://python-poetry.org)
1. **Install Poetry:** find instructions for your system [here](https://python-poetry.org) 
2. **Add [`pyproject.toml`](https://github.com/invap/rt-rabbitmqwrapper/blob/main/pyproject.toml):** the content of the `pyproject.toml` file needed for setting up the project using poetry is shown below.
```toml
[project]
name = "rt-rabbitmq-wrapper"
version = "0.1.0"
description = "This project contains a wrapper for accessing RabbitMQ exchange from The Runtime Monitor constellation of tools."
authors = [
  {name = "Carlos Gustavo Lopez Pombo", email = "clpombo@gmail.com"}
]
license = "SPDX-License-Identifier: AGPL-3.0-or-later"
readme = "README.md"
requires-python = ">=3.11,<4.0"
packages = [
    { include = "rt_rabbitmq_wrapper"},
]
dependencies = [
    "pika (~=1.3.2)",
    "pika-stubs (~=0.1.3)",
    "pip (~=25.1.1)",
    "poetry-core (~=2.1.3)",
]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```
3. **Install the project:** To install the Python project using Poetry, navigate to the directory where the project is and run:
   ```bash	
   poetry install
   ```
4. **Activate the virtual environment**: To activate the virtual environment created by the previous command run:
   ```bash
   poetry env use [your_python_command]
   poetry env activate
   ```
this will ensure you are using the right Python virtual machine and then, activate the virtual environment.


## Linting Python code (with Black)
A linter in Python is a tool that analyzes your code for potential errors, code quality issues, and stylistic inconsistencies. Linters help enforce a consistent code style and identify common programming mistakes, which can improve the readability and maintainability of your code. They’re especially useful in team environments to maintain coding standards.

Though primarily an auto-formatter, `Black` enforces a consistent code style and handles many linting issues by reformatting your code directly.

1. **Activate the virtual environment in your project directory:**
2. **Run linter (black):**
	- For correcting the code:
	```bash
	black .
	```
	- For checking but not correcting the code:
	```bash
	black . --check
	```

## Perform regression testing
Tu run the unit tests of the project use the command `python -m unittest discover -s . -t .`.

When executed, it performs Python unit tests with the `unittest` module, utilizing the `discover` feature to automatically find and execute test files.
- `python -m unittest`:
Runs the `unittest` module as a script. This is a built-in Python module used for testing. When called with `-m`, it allows you to execute tests directly from the command line.
- `discover`:
Tells `unittest` to search for test files automatically. This is useful when you have many test files, as it eliminates the need to specify each test file manually. By default, `unittest` discover will look for files that start with "test" (e.g., `test_example.py`).
- `-s .`:
The `-s` option specifies the start directory for test discovery.
Here, `.` means the current directory, so `unittest` will start looking for tests in the current directory and its subdirectories.
- `-t .`:
The `-t` option sets the top-level directory of the project.
Here, `.` also indicates the current directory. This is mainly useful when the start directory (`-s`) is different from the project's root. For simple projects, the start directory and top-level directory are often the same.

**In summary, this command tells Python’s `unittest` module to:**
Look in the current directory (`-s .`) for any test files that match the naming pattern `test*.py`.
Run all the tests it finds, starting from the current directory (`-t .`) and treating it as the top-level directory.


## Build the application as a library with poetry
To build a package from the Python project follow these steps:
Now that your configuration files are set, you can build the package using poetry running the build command in the root directory of the project:
```bash
poetry build
```
This will create two files in a new `dist` directory:
- A source distribution: [rt_rabbitmq_wrapper-0.1.0.tar.gz](https://github.com/invap/rt-rabbitmq-wrapper/blob/main/dist/rt_rabbitmq_wrapper-0.1.0.tar.gz)
- A wheel distribution: [rt_rabbitmq_wrapper-0.1.0-py3-none-any.whl](https://github.com/invap/rt-rabbitmq-wrapper/blob/main/dist/rt_rabbitmq_wrapper-0.1.0-py3-none-any.whl)


## Install the application as a library locally
Follow the steps below for installing the RR as a local library:
1. **Build the application as a library:**
Follow the steps in Section [Build the application as a library with poetry](#build-the-application-as-a-library-with-poetry)
2. **Install the package locally:** 
Use the command `pip install dist/rt_rabbitmq_wrapper-0.1.0-py3-none-any.whl`.


### Distribute the application as a library
Follow the steps below for distributing the RR as a library in PyPI:
1. **Build the application as a library:**
Follow the steps in Section [Build the application as a library](#build-the-application-as-a-library)
2. **Upload the package to PyPI:**
If you want to make your package publicly available, you can upload it to the Python Package Index (PyPI).
	- Install twine (a tool for uploading packages):
	```bash
	pip install twine
	```
	- Upload the package:
	```bash
	twine upload dist/*
	```
	This command will prompt you to enter your PyPI credentials. Once uploaded, others can install your package with `pip install your-package-name`.


## Using the The Runtime RabbitMQ wrapper for developing other components
As we mentioned in the introduction, The Runtime RabbitMQ wrapper is not meant to be used by its own. Using it in the development of components for The Runtime Monitor tool constellation can be achieved also by configuring the appropriate dependency in the `pyproject.toml` of the components as:
```toml
    "rt-rabbitmq-wrapper @ git+https://github.com/invap/rt-rabbitmq-wrapper.git#main"
```
A specific of tag can be checked out by suffixing the git repository url with `@tag` instead of using a branch name like `#main`.

