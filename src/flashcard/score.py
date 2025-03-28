# Score Elements - mostly, a wrapper for music21

from enum import Enum
import typing

import music21
import music21.midi.translate
from music21.duration import Duration

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
    ionian = 8 # same as major
    aeolian = 9 # same as minor

# All the keys, including enharmonic equivalents
class Key(Enum):
    C = "C"
    Csharp = "C#"
    Dflat = "Db"
    D = "D"
    Dsharp = "D#"
    Eflat = "Eb"
    E = "E"
    F = "F"
    Fsharp = "F#"
    Gflat = "Gb"
    G = "G"
    Gsharp = "G#"
    Aflat = "Ab"
    A = "A"
    Asharp = "A#"
    Bflat = "Bb"
    B = "B"

class KeyAndMode:
    '''Key and mode'''
    def __init__(self, tonic: Key, mode: Mode):
        self.music21_key = music21.key.Key(tonic.name, mode.name)
        self.name = tonic.value + " " + mode.name
    
    def __str__(self):
        return self.name

# circle of fifths
circle = ('C', 'G', 'D', 'A', 'E', 'B', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F')

# root notes where we won't see double flats or sharps for dom7 chords
root_notes = ('A', 'Bb', 'B', 'C', 'C#', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab')

# A Note is a musical note or rest, including adornments like accidentals, articulations, etc.
# Note names consist of a capital letter A-G followed by an optional accidental and octave number,
# where C4 is middle C.  We use this rather than pitch so that the notation is as expected.
# The name of a rest is "rest".
# Unlike music21, our Note has no duration.  We put Notes in Ticks to give duration.
# TODO: Rests NYI

# A note can be initialized from a name (str) or a MIDI note number (int).

class Note:
    '''Note or rest'''
    def __init__(self, name: str, keyAndMode: KeyAndMode=None):
        self.name = name
        if name != "rest":
            # FIXME: should use music21.pitch instead
            self.note = music21.note.Note(name)
            if not isinstance(name, str):
                # it's a MIDI note number
                self.name = self.note.name + str(self.note.octave)
            if keyAndMode is not None:
                # Fix the note to match the key signature
                # FIXME: not working as intended, see test_note_named_note_fix() and test_note_midi_note_fix_flatkey()
                ks = music21.key.KeySignature(keyAndMode.music21_key.sharps)
                self.note.pitch.accidental = ks.accidentalByStep(self.note.pitch.step)
                self.name = self.note.name + str(self.note.octave)

    def __str__(self):
        return self.name
    
    def midi(self):
        '''Return the MIDI number of the note'''
        return self.note.pitch.midi

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

def transpose(pitch:music21.pitch.Pitch, change:str):
    # change is either a Music21 degree (e.g., 'M3', 'm3', 'P5') or a tuple of degrees to apply in order
    degrees = (change,)
    if isinstance(change, tuple):
        degrees = change
    for d in degrees:
        pitch = pitch.transpose(d)
    return pitch

def chord(root: Note, keysig: Key, parts: list[list[str]]):
    '''Return one or two lists of notes for the chord with the given parts (lists of intervals, per clef)'''
    if parts is None:
        return None
    root_pitch = root.note.pitch
    note_parts = []
    for part in parts:
        intervals = [transpose(root_pitch, interval) for interval in part]
        note_parts.append([Note(pitch) for pitch in music21.chord.Chord(intervals).pitches])
    # put treble part first
    note_parts.reverse()
    return note_parts

class Tick:
    '''set of Notes and rests that happen at the same time for the same duration'''
    def __init__(self, duration: Duration, notes: set[Note]=None):
        self.duration = duration
        if notes == None:
            notes = set()
        else:
            self.notes = notes

    def __str__(self):
        # TODO: for now, ignore duration because it's always 1
        # return "Tick " + str(self.duration) + " " + " ".join(sorted([str(n) for n in self.notes]))
        return "Tick " + " ".join(sorted([str(n) for n in self.notes]))
    
    def add(self, notes: set[Note]):
        self.notes.update(notes)

class Sequence:
    '''A sequence of Ticks, all in the same clef'''
    def __init__(self, clef: Clef=None, ticks: list[Tick]=None):
        self.clef = clef
        if ticks == None:
            ticks = []
        self.ticks = ticks
    
    def __str__(self):
        clefstr = "" if self.clef is None else str(self.clef) + " "
        return "Sequence " + clefstr + " ".join([str(t) for t in self.ticks])
    
    def add(self, ticks: list[Tick]):
        '''Add a tick to the sequence'''
        self.ticks.extend(ticks)

class Score:
    '''A set of sequences, typically treble and/or bass clefs'''
    def __init__(self, sequences: list[Sequence]=None, keyAndMode: KeyAndMode=None):
        if sequences == None:
            sequences = []
        self.sequences = sequences
        self.keyAndMode = keyAndMode
    
    def __str__(self):
        return "Score " + " ".join([str(s) for s in self.sequences])
    
    def add(self, sequence: Sequence):
        '''Add a sequence to the system'''
        self.sequences.append(sequence)
    
    def score(self):
        '''Render the system to a score'''
        score = music21.stream.Score()
        for sequence in self.sequences:
            part = music21.stream.Part()
            # FIXME: key signature doesn't appear
            if self.keyAndMode is not None:
                key_sig = music21.key.KeySignature(self.keyAndMode.music21_key.sharps)
                part.append(key_sig)
            match sequence.clef:
                case Clef.Bass:
                    part.append(music21.clef.BassClef())
                case Clef.Treble:
                    part.append(music21.clef.TrebleClef())
            for tick in sequence.ticks:
                chord = music21.chord.Chord([note.note for note in tick.notes])
                part.append(chord)
            score.append(part)
        # TODO: put treble part first, so treble clef is on top in rendering
        return score

    def write(self, filename: str):
        '''Write the score to a file'''
        self.score().write('musicxml', fp=filename)
        print("Wrote '" + filename + "'")

    def toXml(self) -> str:
        # generate XML text rather than writing to file (not working)
        m21_score = self.score()
        return music21.musicxml.m21ToXml.GeneralObjectExporter(m21_score).parse().decode('utf-8')
    
    def toMidi(self) -> bytes:
        m21_score = self.score()
        mf = music21.midi.translate.streamToMidiFile(m21_score)
        midi_bytes = mf.writestr()
        return midi_bytes
    
    def toOutputs(self) -> typing.Tuple[str, bytes]:
        return (self.toXml(), self.toMidi())

if __name__ == '__main__': # pragma: no cover

    import web

    if False:
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

    if False:
        score = Score([treble, bass], keyAndMode=KeyAndMode(Key.C, Mode.mixolydian))
        print(score)
        score.write('output/score.xml')
        web.display_musicxml('score', 'output/score.html', 'output/score.xml')

    if False:
        print("n1 MIDI = ", n1.midi())
        print("Note for MIDI 60: ", str(Note(60)))

        # Show the bass clef with a note above it
        bass_tick = Tick(Duration('quarter'), {Note('D4')})
        bass = Sequence(Clef.Bass, {bass_tick})
        score = Score([bass])
        score.write('output/score-bass-clef.xml')
        web.display_musicxml('score-bass-clef', 'output/score-bass-clef.html', 'output/score-bass-clef.xml')

        # Show the treble clef with a note below it
        treble_tick = Tick(Duration('quarter'), {Note('A3')})
        treble = Sequence(Clef.Treble, {treble_tick})
        score = Score([treble])
        score.write('output/score-treble-clef.xml')
        web.display_musicxml('score-treble-clef', 'output/score-treble-clef.html', 'output/score-treble-clef.xml')

        # chromatic sequence
        seq = Sequence()
        for i in range(60, 72):
            t = Tick(Duration('quarter'), {Note(i)})
            seq.add([t])
        score = Score([seq])
        score.write('output/score-chromatic.xml')
        web.display_musicxml('score-chromatic', 'output/score-chromatic.html', 'output/score-chromatic.xml')

    if False:
        n = Note("C4")
        # FIXME chord now returns a list of parts
        ch = chord(n, Key("C"), [0, 3, 7, 'm9', 'A9'])
        for note in ch:
            print(note)

    if True:
        n1 = Note('C3')
        n2 = Note('C4')
        n3 = Note('Eb4')
        n4 = Note('G4')
        ttick = Tick(Duration('quarter'), {n2, n3, n4})
        btick = Tick(Duration('quarter'), {n1})
        tseq = Sequence(clef=Clef.Treble, ticks={ttick})
        bseq = Sequence(clef=Clef.Bass, ticks={btick})
        score = Score([tseq, bseq])
        if True:
            score.write('output/score-split.xml')
            web.display_musicxml('score-split', 'output/score-split.html', 'output/score-split.xml')
        xml, midi = score.toOutputs()
        # print(xml)

        # play the MIDI
        from midi import midi_play
        midi_play(midi)

