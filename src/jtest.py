from music21 import stream, note, chord, meter

import web

score = stream.Score()
part = stream.Part()
part.append(note.Note('C4', quarterLength=1))  # C4, quarter note
part.append(note.Rest(quarterLength=1))        # Quarter rest
part.append(note.Note('E4', quarterLength=1))  # E4, quarter note
part.append(chord.Chord(['G4', 'B4'], quarterLength=1))  # G4 and B4, quarter chord
score.append(meter.TimeSignature('4/4'))
score.append(part)

score.write('musicxml', 'output/jtest.xml')

# Display the score using OpenSheetMusicDisplay
from IPython.display import display, HTML
import webbrowser
import tempfile
from pathlib import Path

# write the html file
web.display_musicxml('output/jtest.html', 'output/jtest.xml')

# open it in the browser
# NOTE: before running, open a webserver using `python -m http.server` in this directory
webbrowser.open('http://localhost:8000/output/jtest.html')



