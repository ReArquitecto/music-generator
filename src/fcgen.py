# flash-card generators

import random

from score import *
from chords import *

class NoteRange(object):
    def __init__(self, low:Note, high:Note):
        self.low = low
        self.high = high

    def __str__(self):
        return "NoteRange(%d, %d)" % (self.low, self.high)

def random_note(range:NoteRange, keyAndMode:KeyAndMode=None):
    '''Generate a random Note within the given range'''
    low = range.low.midi()
    high = range.high.midi()
    chosen = random.randint(low, high)
    return Note(chosen, keyAndMode)

def fc_randnote(range:NoteRange, clef:Clef=None, keyAndMode:KeyAndMode=None):
    '''Generate a Score for a random quarter note in the given range, clef, and mode'''
    note = random_note(range, keyAndMode)
    tick = Tick(Duration(1), {note})
    seq = Sequence(clef, [tick])
    return Score({seq}, keyAndMode=keyAndMode)

def fc_notes(notes:set[Note], clef:Clef=None, keyAndMode:KeyAndMode=None):
    '''Generate Score for the given sequence of notes, as quarter notes, in the given range, clef, and mode'''
    tick = Tick(Duration(1), notes)
    seq = Sequence(clef, [tick])
    return Score({seq}, keyAndMode=keyAndMode)

def fc_interval(n1:Note, interval:int, clef:Clef=None, keyAndMode:KeyAndMode=None):
    '''Create a Score for the given interval vertically, given note, interval#, clef, and mode'''
    n2 = Note(n1.note.pitch.transpose(interval))
    tick = Tick(Duration(1), {n1, n2})
    seq = Sequence(clef, [tick])
    return Score({seq}, keyAndMode=keyAndMode)

def fc_chord(n1:Note, type:ChordType, voicing:Voicing, key: Key):
    '''Create a Score for the given chord, given root, type, voicing, and key signature'''
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
    return Score(seqs, keyAndMode=KeyAndMode(key, Mode.major))

def fc_write_and_display(score:Score, title:str, html_filename:str, score_filename:str, description:str=""):
    score.write(score_filename)
    web.display_musicxml(title, html_filename, score_filename, description)

def select_key(key:set[Key]):
    '''Select a random key from the given set'''
    return random.choice(list(key))

def select_mode(mode:set[Mode]):
    '''Select a random mode from the given set'''
    return random.choice(list(mode))

if __name__ == "__main__":
    import web

    if True:
        # print a random note
        print("Random note: " + str(random_note(NoteRange(Note("C4"), Note("G4")))))

        # Generate flash cards, each with a random note

        # Note: in the following, the notes are above bass clef to show that bass clef is forced
        score = fc_randnote(NoteRange(Note("C#4"), Note("G4")), Clef.Bass)
        score.write("output/fcgen-note-bass.xml")
        fc_write_and_display(score, "fcgen-note-bass", "output/fcgen-note-bass.html", "output/fcgen-note-bass.xml")

        # Note that this is not the note printed above
        fc_randnote(NoteRange(Note("C4"), Note("G4")))
        score.write("output/fcgen-note.xml")
        fc_write_and_display(score, "fcgen-note", "output/fcgen-note.html", "output/fcgen-note.xml")

    if True:
        # select random key and mode
        keys = {Key.C, Key.D, Key.E, Key.F, Key.G, Key.A, Key.B, Key.Bflat, Key.Eflat, Key.Aflat, Key.Dflat, Key.Gflat}
        modes = {Mode.ionian, Mode.dorian, Mode.phrygian, Mode.lydian, Mode.mixolydian, Mode.aeolian, Mode.locrian}
        modes = {Mode.major} # keep it simple ... any mode works but this way it's easier to see if it makes sense
        kam = KeyAndMode(select_key(keys), select_mode(modes))
        print(kam)
        fc_randnote(NoteRange(Note("A4"), Note("G#5")), keyAndMode=kam)
        score.write("output/fcgen-key.xml")
        fc_write_and_display(score, "fcgen-key", "output/fcgen-key.html", "output/fcgen-key.xml", description=str(kam))
    
    if True:
        # show a chord
        fc_chord(Note("D4"), type=ChordType.dom7, voicing=Voicing.blues, key=Key.C)
        score.write("output/fcgen-chord.xml")
        fc_write_and_display(score, "fcgen-chord", "output/fcgen-chord.html", "output/fcgen-chord.xml", description="D7 in C")
