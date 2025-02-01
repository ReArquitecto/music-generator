# a Note is a musical note or rest, including adornments like accidentals, articulations, etc.
import music21
from music21.duration import Duration
from enum import Enum

# Note names consist of a capital letter A-G followed by an optional accidental and octave number,
# where C4 is middle C.  We use this rather than pitch so that the notation is as expected.
# The name of a rest is "rest".

class Note:
    '''Note or rest'''
    def __init__(self, name):
        self.name = name
        self.note = music21.note.Note(name) if name != 'rest' else music21.note.Rest()

    def __str__(self):
        return self.name
    
class Tick:
    '''Notes and rests that happen at the same time for the same duration,
    an unordered set of Notes'''
    def __init__(self, duration: Duration, notes: set[Note]={}):
        self.duration = duration
        self.notes = notes

    def __str__(self):
        return "Tick " + str(self.duration) + " " + " ".join([str(n) for n in self.notes])
    
    def add(self, notes: set[Note]):
        self.notes.update(notes)

class Sequence:
    '''A sequence of Ticks, all in the same clef'''
    def __init__(self, clef=None, ticks: list[Tick]=[]):
        self.clef = clef
        self.ticks = ticks
    
    def __str__(self):
        clefstr = "" if self.clef is None else str(self.clef) + " "
        return "Sequence " + clefstr + " ".join([str(t) for t in self.ticks])
    
    def add(self, ticks: list[Tick]=[]):
        '''Add a tick to the sequence'''
        self.ticks.extend(ticks)

class Score:
    '''A set of sequences, typically treble and/or bass clefs'''
    def __init__(self, sequences: set[Sequence]={}):
        self.sequences = sequences
    
    def __str__(self):
        return "System " + " ".join([str(s) for s in self.sequences])
    
    def add(self, sequence: Sequence):
        '''Add a sequence to the system'''
        self.sequences.extend(sequence)
    
    def score(self):
        '''Render the system to a score'''
        score = music21.stream.Score()

        for sequence in self.sequences:
            part = music21.stream.Part()
            for tick in sequence.ticks:
                chord = music21.chord.Chord([note.note for note in tick.notes])
                part.append(chord)
            score.append(part)
        return score

if __name__ == '__main__':
    n1 = Note('C4')
    n2 = Note('Eb4')
    n3 = Note('G4')
    treble_tick = Tick(Duration('quarter'), {n1, n2})
    treble_tick.add({n3})
    print("Treble tick:", treble_tick)

    n4 = Note('C3')
    bass_tick = Tick(Duration('quarter'), {n4})
    print("Bass tick:", bass_tick)
    
    treble = Sequence(ticks=[treble_tick])
    print("Treble sequence:", treble)
    treble.add([Tick(Duration('quarter'), {Note('C4')})])

    bass = Sequence(music21.clef.BassClef, {bass_tick})
    print("Bass sequence:", bass)

    score = Score([treble, bass])
    print(score)
    score.score().write('musicxml', fp='output/score.xml')
