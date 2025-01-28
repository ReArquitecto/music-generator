# Introduction
This repository contains projects for automating processes in the PM Back Office

# Setup
It's best to run this project in a virtual environment. So please follow these steps:

## Virtual Environment
To setup your virtual Python environment, please
- Make sure you have Python 3 installed
- Clone the repository
- Navigate to the project directory in the terminal
- In the terminal:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

## Add Virtual Environment to VS Code
Microsoft VS Code automatically starts the virtual environment when you open the project, but only after you have followed these steps: 
- Press Ctrl+Shift+P and type “Python: Select Interpreter.”
- Choose the interpreter from the .venv directory to ensure VS Code uses your virtual environment for the project.

If you're running a different IDE, you will probably want to look up how to do this for your IDE. If you don't enable this in your IDE or are unable to do so, you'll have to start the environment from the terminal as needed.

## Install Project Dependencies
In the terminal:
```bash
pip install -r requirements.txt
```

## Development
If at anytime during development you install more dependencies for the projects, you can run the following to add them to the requirements.txt.

In the terminal:
```bash
pip install -r requirements.txt
pip freeze > requirements.txt
```

# Features
TODO: Finish this readme file
