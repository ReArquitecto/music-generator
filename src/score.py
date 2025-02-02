# a Note is a musical note or rest, including adornments like accidentals, articulations, etc.
import music21
from music21.duration import Duration
from enum import Enum

class Clef(Enum):
    '''Clef types'''
    Treble = 1
    Bass = 2
    Piano = None    # Both treble and bass

class Mode(Enum):
    '''Mode types'''
    major = 1
    minor = 2
    mixolydian = 3
    dorian = 4
    phrygian = 5
    lydian = 6
    locrian = 7
    ionian = 8
    aeolian = 9

class Key:
    '''Key and mode'''
    def __init__(self, tonic: str, mode: Mode):
        self.music21_key = music21.key.Key(tonic, mode.name)
    
    def __str__(self):
        return "Key " + str(self.key)
    

# A Note is a musical note or rest, including adornments like accidentals, articulations, etc.
# Note names consist of a capital letter A-G followed by an optional accidental and octave number,
# where C4 is middle C.  We use this rather than pitch so that the notation is as expected.
# The name of a rest is "rest".

# A note can be initialized from a name (str) or a MIDI note number (int).

class Note:
    '''Note or rest'''
    def __init__(self, name: str):
        self.name = name
        self.note = music21.note.Note(name) if name != 'rest' else music21.note.Rest()
        if not isinstance(name, str):
            self.name = self.note.name + str(self.note.octave)

    def __str__(self):
        return self.name
    
    def midi(self):
        '''Return the MIDI number of the note'''
        return self.note.pitch.midi
    
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
    def __init__(self, clef: Clef=None, ticks: list[Tick]=[]):
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
    def __init__(self, sequences: set[Sequence]={}, key: Key=None):
        self.sequences = sequences
        self.key = key
    
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
            if self.key is not None:
                part.append(self.key.music21_key)
            match sequence.clef:
                case Clef.Bass:
                    part.append(music21.clef.BassClef())
                case Clef.Treble:
                    part.append(music21.clef.TrebleClef())
            for tick in sequence.ticks:
                chord = music21.chord.Chord([note.note for note in tick.notes])
                part.append(chord)
            score.append(part)
        return score
    
    def write(self, filename: str):
        '''Write the score to a file'''
        self.score().write('musicxml', fp=filename) 
        print("Wrote '" + filename + "'")

if __name__ == '__main__':
    n1 = Note('C4')
    n2 = Note('Eb4')
    n3 = Note('G4')
    treble_tick = Tick(Duration('quarter'), {n2})
    treble_tick.add({n3})
    print("Treble tick:", treble_tick)

    n4 = Note('C3')
    bass_tick = Tick(Duration('quarter'), {n1, n4})
    print("Bass tick:", bass_tick)
    
    treble = Sequence(ticks=[treble_tick])
    print("Treble sequence:", treble)
    treble.add([Tick(Duration('quarter'), {Note('C4')})])

    bass = Sequence(Clef.Bass, {bass_tick})
    print("Bass sequence:", bass)

    score = Score([treble, bass], key=Key('C', Mode.mixolydian))
    print(score)
    score.write('output/score.xml')

    print("n1 MIDI = ", n1.midi())
    print("Note for MIDI 60: ", str(Note(60)))

    # Show the bass clef with a note above it
    bass_tick = Tick(Duration('quarter'), {Note('D4')})
    bass = Sequence(Clef.Bass, {bass_tick})
    score = Score([bass])
    score.write('output/score-bass-clef.xml')

    # Show the treble clef with a note below it
    treble_tick = Tick(Duration('quarter'), {Note('A3')})
    treble = Sequence(Clef.Treble, {treble_tick})
    score = Score([treble])
    score.write('output/score-treble-clef.xml')

    # chromatic sequence
    seq = Sequence()
    for i in range(60, 72):
        t = Tick(Duration('quarter'), {Note(i)})
        seq.add([t])
    score = Score([seq])
    score.write('output/score-chromatic.xml')
