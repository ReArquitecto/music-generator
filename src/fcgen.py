# flash-card generators

import random
from score import *

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

def fc_note(fname:str, range:NoteRange, clef:Clef=None, keyAndMode:KeyAndMode=None):
    note = random_note(range, keyAndMode)
    tick = Tick(Duration(1), {note})
    sequence = Sequence(clef, [tick])
    score = Score({sequence}, keyAndMode=keyAndMode)
    score.write(fname)

def select_key(key:set(Key)):
    '''Select a random key from the given set'''
    return random.choice(list(key))

def select_mode(mode:set(Mode)):
    '''Select a random mode from the given set'''
    return random.choice(list(mode))

if __name__ == "__main__":
    import web

    if False:
        # print a random note
        print("Random note: " + str(random_note(NoteRange(Note("C4"), Note("G4")))))

        # Generate flash cards, each with a random note

        # Note: in the following, the notes are above bass clef to show that bass clef is forced
        fc_note("output/fcgen-note-bass.xml", NoteRange(Note("C#4"), Note("G4")), Clef.Bass)
        web.display_musicxml("fcgen-note-bass", "output/fcgen-note-bass.html", "output/fcgen-note-bass.xml")

        # Note that this is not the note printed above
        fc_note("output/fcgen-note.xml", NoteRange(Note("C4"), Note("G4")))
        web.display_musicxml("fcgen-note", "output/fcgen-note.html", "output/fcgen-note.xml")

    # select random key and mode
    # FIXME: some strange cases appear, like F# for Gb major.  Not yet sure what the best approach might be.
    # Consider using accidentlByStep: https://www.music21.org/music21docs/usersGuide/usersGuide_15_key.html#example-adjusting-notes-to-fit-the-key-signature
    keys = {Key.C, Key.D, Key.E, Key.F, Key.G, Key.A, Key.B, Key.Bflat, Key.Eflat, Key.Aflat, Key.Dflat, Key.Gflat}
    modes = {Mode.ionian, Mode.dorian, Mode.phrygian, Mode.lydian, Mode.mixolydian, Mode.aeolian, Mode.locrian}
    modes = {Mode.major} # keep it simple ... any mode works but this way it's easier to see if it makes sense
    kam = KeyAndMode(select_key(keys), select_mode(modes))
    print(kam)
    fc_note("output/fcgen-key.xml", NoteRange(Note("A4"), Note("G#5")), keyAndMode=kam)
    web.display_musicxml("fcgen-key", "output/fcgen-key.html", "output/fcgen-key.xml", description=str(kam))

