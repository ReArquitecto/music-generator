from music21 import stream, note, chord, meter, key

import web

score = stream.Score()
part = stream.Part()
# part.append(key.Key('C', 'mixolydian'))
k = key.Key('Bb', 'major')
ks = key.KeySignature(k.sharps)
part.append(ks)
part.append(note.Note('B', quarterLength=1))
part.append(note.Note('Bb', quarterLength=1))

# FIXME: some strange cases appear, like F# for Gb major.  Not yet sure what the best approach might be.
# Consider using accidentlByStep: https://www.music21.org/music21docs/usersGuide/usersGuide_15_key.html#example-adjusting-notes-to-fit-the-key-signature
# n.pitch.accidental = ks.accidentalByStep(n.pitch.step)
for n in part.notes:
    n.pitch.accidental = n.getContextByClass(key.KeySignature).accidentalByStep(n.step)

# core.append(part)
# score.write('musicxml', 'output/jtest.xml')
# web.display_musicxml('jtest', 'output/jtest.html', 'output/jtest.xml')

if False:

    s1 = stream.Stream()
    s1.append(key.KeySignature(4))  # E-major or C-sharp-minor
    s1.append(note.Note('C', type='half'))
    s1.append(note.Note('E-', type='half'))
    s1.append(key.KeySignature(-4))  # A-flat-major or F-minor
    s1.append(note.Note('A', type='whole'))
    s1.append(note.Note('F#', type='whole'))

    for n in s1.notes:
        n.pitch.accidental = n.getContextByClass(key.KeySignature).accidentalByStep(n.step)

    s1.write('musicxml', 'output/jtest.xml')
    web.display_musicxml('jtest', 'output/jtest.html', 'output/jtest.xml')

if False:
    def generate_chord(root_note, key_signature, intervals):
        k = key.Key(key_signature)
        ks = key.KeySignature(k.sharps)
        chord_notes = [note.Note(root_note)]
        
        for interval in intervals:
            n = note.Note()
            n.transpose(interval, inPlace=True)
            chord_notes.append(n)
        
        for n in chord_notes:
            n.pitch.accidental = ks.accidentalByStep(n.step)
        
        return chord.Chord(chord_notes)

    # Example usage:
    root = 'C'
    key_sig = 'C major'
    intervals = ['M3', 'P5']
    ch = generate_chord(root, key_sig, intervals)
    print(ch)

if True:
    s1 = stream.Stream()
    s1.append(note.Note('C4', type='half'))
    s1.append(note.Note('C3', type='half'))
    s1.append(note.Note('C2', type='half'))

    s1.write('musicxml', 'output/jtest.xml')
    web.display_musicxml('jtest', 'output/jtest.html', 'output/jtest.xml')
