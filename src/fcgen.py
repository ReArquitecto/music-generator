# flash-card generators

import random
from score import *

class NoteRange(object):
    def __init__(self, low:Note, high:Note):
        self.low = low
        self.high = high

    def __str__(self):
        return "NoteRange(%d, %d)" % (self.low, self.high)

def random_note(range:NoteRange):
    '''Generate a random Note within the given range'''
    low = range.low.midi()
    high = range.high.midi()
    chosen = random.randint(low, high)
    return Note(chosen)

def fc_note(fname:str, range:NoteRange, clef:Clef=None):
    note = random_note(range)
    tick = Tick(Duration(1), {note})
    sequence = Sequence(clef, [tick])
    score = Score({sequence})
    score.write(fname)

if __name__ == "__main__":
    print("Random note: " + str(random_note(NoteRange(Note("C4"), Note("G4")))))
    fc_note("output/fcgen-note.xml", NoteRange(Note("C4"), Note("G4")))
    # Note: in the following, the notes are above bass clef to show that bass clef is forced
    fc_note("output/fcgen-note-bass.xml", NoteRange(Note("C#4"), Note("G4")), Clef.Bass)


