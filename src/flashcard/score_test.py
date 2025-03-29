import pytest
import typing

import music21

from flashcard.score import *
from flashcard import chords

def test_KeyAndMode():
    kam = KeyAndMode(Key('C'), mode=Mode.major)
    assert kam.name == 'C major'

    assert str(kam) == kam.name

def test_note_no_octave():
    n = Note('C')
    assert n.name == 'C'
    assert n.note.octave == None # FIXME: we shouldn't support notes without octave specified

def test_note_octave():
    n = Note('C4')
    assert n.name == 'C4'
    assert str(n) == n.name
    assert n.note.octave == 4

def test_note_midi():
    n = Note(60)
    assert n.name == 'C4'

def test_note_midi_note_fix_sharpkey():
    # make sure the note is a flat for a flat key and sharp for a sharp key
    n = Note(61, KeyAndMode(Key.B, Mode.major))
    assert n.name == 'C#4'
    assert n.midi() == 61

@pytest.mark.skip # For Bb major, 61 should be Db, not C#
def test_note_midi_note_fix_flatkey():
    # make sure the note is a flat for a flat key and sharp for a sharp key
    n = Note(61, KeyAndMode(Key.Bflat, Mode.major))
    assert n.name == 'Db4'
    assert n.midi() == 61

@pytest.mark.skip # Db should be changed to C#, but we don't actually use this case.
def test_note_named_note_fix():
    n = Note('Db4', KeyAndMode(Key.B, Mode.major))
    if False:
        # FIXME
        assert n.name == 'C#4'

def test_note_equal():
    n = Note('C4')
    assert n != None
    assert n != Note('C5')
    assert n.__hash__() == hash(n.name)

transpose_table = (
    # (initial, interval, final)
    # remember music21 uses '-' for flat
    ('C4', 'm2', 'D-4'),
    ('C4', 'M2', 'D4'),
    ('C4', 'm3', 'E-4'),
    ('C4', 'M3', 'E4'),
    ('C4', 'P4', 'F4'),
    ('C4', 'd5', 'G-4'),
    ('C4', 'P5', 'G4'),
    ('C4', 'a5', 'G#4'),
    ('C4', 'm6', 'A-4'),
    ('C4', 'M6', 'A4'),
    ('C4', 'd7', 'B--4'), # we could "fix" it to return A
    ('C4', 'm7', 'B-4'),
    ('C4', 'M7', 'B4'),
    ('C4', 'P8', 'C5'),

    ('B3', 'm2', 'C4'),
    ('B3', 'M2', 'C#4'),
    ('B3', 'm3', 'D4'),
    ('B3', 'M3', 'D#4'),
    ('B3', 'P4', 'E4'),
    ('B3', 'd5', 'F4'),
    ('B3', 'P5', 'F#4'),
    ('B3', 'a5', 'F##4'), # we could "fix" it to return G4
    ('B3', 'm6', 'G4'),
    ('B3', 'M6', 'G#4'),
    ('B3', 'd7', 'A-4'),
    ('B3', 'm7', 'A4'),
    ('B3', 'M7', 'A#4'),
    ('B3', 'P8', 'B4'),

    ('C4', ('P-8', 'm7'), 'B-3'),
)

def test_note_transpose():
    for (initial, change, final) in transpose_table:
        p1 = music21.pitch.Pitch(initial)
        p2 = transpose(p1, change)
        assert  p2.nameWithOctave == final, f"transposing {initial} by {change} to get {final}, got {p2.nameWithOctave}"

def test_score_chord_noparts():
    ch = chord(Note('C4'), None, None)
    assert ch == None

def show_part(part:typing.List[Note]) -> str:
    return '(' + ','.join([str(n) for n in part]) + ')'

def show_parts(parts) -> str:
    if parts == None:
        return "No parts"
    if len(parts) == 0:
        return '[]'
    out = '['
    out += ','.join([show_part(part) for part in parts])
    return out + ']'

def test_score_chord():
    chord_table = (
        # root, Voicing, ChordType, result
        ('C4', chords.Voicing.standard, 'maj', [('C4', 'E4', 'G4')]),
        ('C4', chords.Voicing.standard, 'min', [('C4', 'E-4', 'G4')])
    )

    for (root, voicing, ch_type, result) in chord_table:
        n = Note(root)
        result_notes = []
        for part in result:
            notes = [Note(nname) for nname in part]
            result_notes.append(notes)
        rel_parts = chords.Chord(chords.ChordType(ch_type), voicing).parts
        parts = chord(n, None, rel_parts)
        assert parts == result_notes, f"expected {show_parts(result_notes)}, got {show_parts(parts)}"

def test_tick():
    qn = music21.duration.Duration(1)
    t = Tick(qn, None)
    t = Tick(qn, set((Note('C4'),)))
    assert t.duration == qn
    s = str(t)
    # TODO: for now, ignore duration because it's always 1
    # assert s == "Tick " + str(qn) + " C4"
    assert s == "Tick C4"

    t.add(set((Note('D4'),)))
    # TODO: for now, ignore duration because it's always 1
    # assert str(t) == "Tick " + str(qn) + " C4 D4"
    assert str(t) == "Tick C4 D4"

def test_sequence():
    s = Sequence()
    assert s.clef == None
    assert len(s.ticks) == 0

    qn = music21.duration.Duration(1)
    t = Tick(duration=qn, notes=set((Note('C4'),)))
    seq = Sequence(ticks=[t])
    assert len(seq.ticks) == 1

    t2 = Tick(duration=qn, notes=set((Note('D4'),)))
    seq.add(set((t2,)))

    assert str(seq) == "Sequence Tick C4 Tick D4"

def test_score(tmpdir:str):
    s = Score()
    assert len(s.sequences) == 0
    assert s.keyAndMode == None

    qn = music21.duration.Duration(1)
    t = Tick(qn, set((Note('C4'),)))
    tseq = Sequence(Clef.Treble, ticks=[t])
    s = Score([tseq], keyAndMode=KeyAndMode(Key('C'), Mode.major))
    assert len(s.sequences) == 1
    assert s.keyAndMode.name == "C major"

    bseq = Sequence(Clef.Bass, ticks=[t])
    s.add(bseq)
    assert len(s.sequences) == 2
    assert str(s) == "Score Sequence Clef.Treble Tick C4 Sequence Clef.Bass Tick C4"

    m21score = s.score()
    s.write("output/test_score.xml" )

    xml, midi = s.toOutputs()

