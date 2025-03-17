# Score Elements - mostly, a wrapper for music21

# a Note is a musical note or rest, including adornments like accidentals, articulations, etc.
import music21
from music21.duration import Duration
from enum import Enum
import tempfile
import webbrowser
from pathlib import Path
import sys

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

# chromatic scale using sharps
chromatic_sharps = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B' )

def notes_in_keysig(key: str):
    """return all the notes in a chromatic scale (not necessariy in order) for the
    given (major) key, using sharps or flats as appropriate for the key."""
    match key:
        case 'C#' |'D' | 'D#' | 'E' | 'F#' | 'G' | 'G#' | 'A' | 'A#' | 'B':
            return chromatic_sharps
        case 'C':
            return ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'Bb')
        case _:
            return circle

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
                self.name = self.note.name + str(self.note.octave)
            if keyAndMode is not None:
                # Fix the note to match the key signature
                ks = music21.key.KeySignature(keyAndMode.music21_key.sharps)
                self.note.pitch.accidental = ks.accidentalByStep(self.note.pitch.step)
                self.name = self.note.name + str(self.note.octave)

    def __str__(self):
        return self.name
    
    def midi(self):
        '''Return the MIDI number of the note'''
        return self.note.pitch.midi

def transpose(pitch:music21.pitch.Pitch, degree:str):
    return pitch.transpose(degree)

def chord(root: Note, keysig: Key, parts: list[list[str]]):
    '''Return one or two lists of notes for the chord with the given parts (lists of intervals, per hand)'''
    if parts is None:
        return None
    # k = music21.key.Key(keysig.name)
    # root_note = k.pitchFromDegree(k.getScaleDegreeFromPitch(root_pitch))
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
        self.notes = notes

    def __str__(self):
        return "Tick " + str(self.duration) + " " + " ".join([str(n) for n in self.notes])
    
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
        return "System " + " ".join([str(s) for s in self.sequences])
    
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
        return score
    
    def split_clefs(self, note:Note=None): # NOTE: not currently used
        '''split score into bass and treble clefs'''
        if len(self.sequences) != 1:
            return self
        
        old_seq = next(iter(self.sequences))
        if old_seq.clef != Clef.Treble and old_seq.clef != None:
            return self
        
        score = Score(keyAndMode=self.keyAndMode)
        treb = Sequence(clef=Clef.Treble)
        bass = Sequence(clef=Clef.Bass)
        for old_tick in old_seq.ticks:
            treb_notes = set()
            bass_notes = set()
            for note in old_tick.notes:
                if note.note.pitch.midi >= music21.pitch.Pitch('C4').midi: # FIXME should use note parameter
                    treb_notes.add(note)
                else:
                    bass_notes.add(note)
            if treb_notes:
                treb.add([Tick(old_tick.duration, treb_notes)])
            if bass_notes:
                bass.add([Tick(old_tick.duration, bass_notes)])
        score.add(treb)
        score.add(bass)
        return score

    def write(self, filename: str):
        '''Write the score to a file'''
        self.score().write('musicxml', fp=filename)
        print("Wrote '" + filename + "'")

    def toXml(self):
        # generate XML text rather than writing to file (not working)
        m21_score = self.score()
        return music21.musicxml.m21ToXml.GeneralObjectExporter(m21_score).parse().decode('utf-8')

if __name__ == '__main__':
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
        n1 = Note('C4')
        n2 = Note('Eb4')
        n3 = Note('G4')
        n4 = Note('C3')
        tick = Tick(Duration('quarter'), {n1, n2, n3, n4})
        seq = Sequence(clef=None, ticks={tick})
        score = Score({seq})
        score = score.split_clefs()
        score.write('output/score-split.xml')
        # web.display_musicxml('score-split', 'output/score-split.html', 'output/score-split.xml')
        print(str(score.toXml()))
