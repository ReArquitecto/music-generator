from music21 import stream, note, chord, meter
from common import get_filename

# Create a Stream (a container for notes, chords, etc.)
score = stream.Score()

# Create a part
part = stream.Part()
part.append(meter.TimeSignature('4/4'))

# Add notes and chords
part.append(note.Note('C4', quarterLength=1))  # C4, quarter note
part.append(note.Rest(quarterLength=1))        # Quarter rest
part.append(note.Note('E4', quarterLength=1))  # E4, quarter note
part.append(chord.Chord(['G4', 'B4'], quarterLength=1))  # G4 and B4, quarter chord

# Add the part to the score
score.append(part)

# Add name
filename = get_filename(ext='xml', user_input=False, prefix='music21')

# Save the score to MusicXML
score.write('musicxml', fp=f'output/{filename}.xml')
