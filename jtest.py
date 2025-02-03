from music21 import stream, note, chord, meter

score = stream.Score()
part = stream.Part()
part.append(note.Note('C4', quarterLength=1))  # C4, quarter note
part.append(note.Rest(quarterLength=1))        # Quarter rest
part.append(note.Note('E4', quarterLength=1))  # E4, quarter note
part.append(chord.Chord(['G4', 'B4'], quarterLength=1))  # G4 and B4, quarter chord
score.append(meter.TimeSignature('4/4'))
score.append(part)

# Display the score using OpenSheetMusicDisplay
from IPython.display import display, HTML
import webbrowser
import tempfile
from pathlib import Path

'''Display the score using OpenSheetMusicDisplay'''
score.write('musicxml', 'output/jtest.xml')

# TODO: write the html file %%%

if False:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_html:
        tmp_html.write(html.encode('utf-8'))
        webbrowser.open(tmp_html.name)

# NOTE: before running, open a webserver using `python -m http.server` in this directory
webbrowser.open('http://localhost:8000/output/jtest.html')



