# Introduction
This repository provides methods to generate musical flash cards in MusicXML format, suitable for use in a program like Piano Marvel.

Given a set of input choices, such as
- number of notes
- chord vs sequential
- key signature
- note range or clef(s)

generate the MusicXML for that note, chord, or sequence of notes.

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

# TEMPORARY development notes

Pytest UT is planned but not yet added.  To test any given file, run it and it's main will exercise the primary features provided by the file.

For convenience, the generated MusicXML files are displayed in your browswer, but first you must start a server in the repo directory:
```bash
python src/server.py &
```

To generate a complet set of flashcards, run fc_gen.py.  View them in your browser at
[http://localost:8000/output/html](http://localost:8000/output/html)

# Plans/Hopes

- [ ] refactor for better use by PM (e.g. fc_gen shouldn't display the output)
- [x] generate flashcards in xml (and html just for local viewing), in all key signatures:
  - [x] single notes
  - [x] intervals (m3, 3, 4, b5, 5, 6, and octave)
  - [ ] non-inverted triads
    - [ ] maj
    - [ ] min
    - [ ] maj7
    - [ ] min7
    - [ ] 7

- [ ] multiple notes
- [ ] chord vs. sequence
- [ ] modes?
- [ ] control panel
- [ ] MIDI input, to check and proceed to next flashcard
- [ ] hosted website
