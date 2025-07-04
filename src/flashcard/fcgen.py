# flash-card generators

import random

from flashcard.score import *
from flashcard.chords import *

class NoteRange(object):
    def __init__(self, low:Note, high:Note):
        self.low = low
        self.high = high

    def __str__(self):
        return f"NoteRange({self.low},{self.high})"

def random_note(range:NoteRange, keyAndMode:KeyAndMode=None):
    '''Generate a random Note within the given range'''
    low = range.low.midi()
    high = range.high.midi()
    chosen = random.randint(low, high)
    return Note(chosen, keyAndMode)

def fc_randnote(range:NoteRange, clef:Clef=None, keyAndMode:KeyAndMode=None) -> typing.Tuple[str, str]:
    '''Generate musicXml and MIDI for a random quarter note in the given range, clef, and mode'''
    note = random_note(range, keyAndMode)
    tick = Tick(Duration(1), {note})
    seq = Sequence(clef, [tick])
    return Score((seq,), keyAndMode=keyAndMode).toOutputs()

def fc_notes(notes:list[Note], clef:Clef=None, keyAndMode:KeyAndMode=None) -> typing.Tuple[str, str]:
    '''Generate musicXml and MIDI for the given sequence of notes, as quarter notes, in the given range, clef, and mode'''
    tick = Tick(Duration(1), notes)
    seq = Sequence(clef, [tick])
    return Score((seq,), keyAndMode=keyAndMode).toOutputs()

def fc_interval(n1:Note, interval:int, clef:Clef=None, keyAndMode:KeyAndMode=None) -> typing.Tuple[str, str]:
    '''Create musicXml and MIDI for the given interval vertically, given note, interval#, clef, and mode'''
    n2 = Note(n1.note.pitch.transpose(interval))
    tick = Tick(Duration(1), {n1, n2})
    seq = Sequence(clef, [tick])
    return Score((seq,), keyAndMode=keyAndMode).toOutputs()

def fc_chord(n1:Note, type:ChordType, voicing:Voicing, key: Key) -> typing.Tuple[str, str]:
    '''Create musicXml and MIDI for the given chord, given root, type, voicing, and key signature'''
    ch = Chord(type, voicing)
    parts = chord(n1, key, ch.parts)
    # parts is a list of parts, where a part is a list of notes.
    if parts is None:
        return None
    seqs = []
    for part in parts:
        tick = Tick(Duration(1), part)
        # treble part is first (or only)
        if len(seqs) == 0:
            clef = Clef.Treble
        else:
            clef = Clef.Bass
        seq = Sequence(clef, [tick])
        seqs.append(seq)
    return Score(seqs, keyAndMode=KeyAndMode(key, Mode.major)).toOutputs()


def select_key(key:set[Key]):
    '''Select a random key from the given set'''
    return random.choice(list(key))

def select_mode(mode:set[Mode]):
    '''Select a random mode from the given set'''
    return random.choice(list(mode))

if __name__ == "__main__": # pragma: no cover
    import web

    if False:
        # print a random note
        print("Random note: " + str(random_note(NoteRange(Note("C4"), Note("G4")))))

        # Generate flash cards, each with a random note

        # Note: in the following, the notes are above bass clef to show that bass clef is forced
        (scoreXml, scoreMidi) = fc_randnote(NoteRange(Note("C#4"), Note("G4")), Clef.Bass)
        web.write_and_display_musicxml(scoreXml, "fcgen-note-bass", "output/fcgen-note-bass.html", "output/fcgen-note-bass.xml")

        # Note that this is not the note printed above
        (scoreXml, scoreMidi) = fc_randnote(NoteRange(Note("C4"), Note("G4")))
        web.write_and_display_musicxml(scoreXml, "fcgen-note", "output/fcgen-note.html", "output/fcgen-note.xml")

    if False:
        # select random key and mode
        keys = {Key.C, Key.D, Key.E, Key.F, Key.G, Key.A, Key.B, Key.Bflat, Key.Eflat, Key.Aflat, Key.Dflat, Key.Gflat}
        modes = {Mode.ionian, Mode.dorian, Mode.phrygian, Mode.lydian, Mode.mixolydian, Mode.aeolian, Mode.locrian}
        modes = {Mode.major} # keep it simple ... any mode works but this way it's easier to see if it makes sense
        kam = KeyAndMode(select_key(keys), select_mode(modes))
        print(kam)
        (scoreXml, scoreMidi) = fc_randnote(NoteRange(Note("A4"), Note("G#5")), keyAndMode=kam)
        web.write_and_display_musicxml(scoreXml, "fcgen-key", "output/fcgen-key.html", "output/fcgen-key.xml", description=str(kam))
    
    if True:
        # show a chord
        note = Note("C4")
        ct = ChordType.dom7
        key = Key.C
        voicing = Voicing.blues
        (scoreXml, scoreMidi) = fc_chord(note, type=ct, voicing=voicing, key=key)
        web.write_and_display_musicxml(scoreXml, "fcgen-chord", "output/fcgen-chord.html", "output/fcgen-chord.xml", description=f"{voicing} {note} {ct} in {key}")
