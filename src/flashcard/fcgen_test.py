import pytest
import re
import typing

import music21

from flashcard.fcgen import *
from flashcard.score import *
from flashcard import chords

def test_noterange():
    nr = NoteRange(Note('C4'), Note('C5'))
    assert str(nr.low) == 'C4'
    assert str(nr.high) == 'C5'
    assert str(nr) == "NoteRange(C4,C5)"

def test_random_note():
    nr = NoteRange(Note('C4'), Note('C5'))
    randnote = random_note(nr)
    assert isinstance(randnote, Note)


@pytest.mark.skip # Note() isn't working correctly yet regarding sharps & flats based on mode
@pytest.mark.timeout(10)
def test_random_note_coverage():
    # generate random notes until we hit them all
    nr = NoteRange(Note('C4'), Note('C5'))
    notes = set() # set of names of notes found
    # while len(notes) < len(Key) + 1:
    for n in range(1,100):
        randnote = random_note(nr, keyAndMode=KeyAndMode(Key('C'), Mode.minor))
        name = str(randnote)
        notes.update((name,))
    
    # show what notes we found
    assert str(sorted(notes)) == ""

def test_fc_randnote():
    nr = NoteRange(Note('C4'), Note('C5'))
    xml, midi = fc_randnote(nr)
    assert type(xml) == str
    assert type(midi) == bytes

def xml_ll_note_re(note, octave, alter):
    """(low level) return RE for given note, octave, and alteration (-1, 0, +1 for flat, natural, sharp)"""
    pattern = r".*?" + f"<step>{note}</step>"
    if alter != 0:
        pattern += r"\s*?" + f"<alter>{alter}</alter>"
    pattern += r"\s*?" + f"<octave>{octave}</octave>"
    return pattern

def xml_note_re(note):
    """return RE for given note (with b/# and octave #)"""
    basenote = note[0]
    alter = 0
    octave_index = 1
    if note[1] == '#':
        alter = +1
        octave_index = 2
    elif note[1] == 'b':
        alter = -1
        octave_index = 2
    octave = int(note[octave_index])
    return xml_ll_note_re(basenote, octave, alter)

def test_fc_notes():
    notes = [
        Note('C4'),
        Note('D#4'),
        Note('Eb4'),
    ]
    xml, midi = fc_notes(notes)
    pattern = (
        xml_ll_note_re('C', 4, 0)
        + xml_ll_note_re('D', 4, 1)
        + xml_ll_note_re('E', 4, -1)
    )
    # assert xml == ""
    # assert pattern == ""
    assert re.search(pattern, xml, flags=re.DOTALL) != None, xml

def test_fc_interval():

    table = (
        # notename, interval, expnote, expoctave, expalter
        ('C4', 'm2', 'D', 4, -1),
        ('C4', 'M2', 'D', 4, 0),
        ('C4', 'm3', 'E', 4, -1),
        ('C4', 'M3', 'E', 4, 0),
        ('C4', 'P4', 'F', 4, 0),
        ('C4', 'd5', 'G', 4, -1),
        ('C4', 'P5', 'G', 4, 0),
        ('C4', 'a5', 'G', 4, +1),
        ('C4', 'm6', 'A', 4, -1),
        ('C4', 'M6', 'A', 4, 0),
        ('C4', 'm7', 'B', 4, -1),
        ('C4', 'M7', 'B', 4, 0),
        ('C4', 'P8', 'C', 5, 0),
    )
    for (notename, interval, expnote, expoctave, expalter) in table:
        xml, midi = fc_interval(Note(notename), interval)

        # check for the 2nd note
        # TODO check for the original note too
        pattern = xml_ll_note_re(expnote, expoctave, expalter)

        assert re.search(pattern, xml, flags=re.DOTALL) != None, (
            f"didn't find {expnote}{expoctave}[{expalter}] for {notename} {interval} interval")

def test_fc_chord():
    table = (
        # root, type, voicing, key, [expected notes]
        ('C4', ChordType.min, Voicing.standard, 'C', ['C4', 'Eb4', 'G4']),
        ('C4', ChordType.dom7, Voicing.blues, 'C', ['C3', 'Bb3', 'E4', 'G4']),

        # TODO: add more, especially problematic ones, when we find bugs
    )
    for (root, type, voicing, key, expected_notes) in table:
        n = Note(root)
        k = Key(key)
        xml, midi = fc_chord(n, type, voicing, k)
        pattern = ""
        for expnote in expected_notes:
            pattern += xml_note_re(expnote)

def test_fc_chord_none():
    result = fc_chord(Note('C4'), ChordType.maj, Voicing.blues, Key('C'))
    assert result == None

@pytest.mark.timeout(1)
def test_select_key():
    keys = set()
    
    for k in Key:
        keys.update((k,))
    
    selected_keys = set()
    while len(selected_keys) < len(Key):
        k = select_key(keys)
        selected_keys.update((k,))

@pytest.mark.timeout(1)
def test_select_mode():
    modes = set()
    
    for m in Mode:
        modes.update((m,))
    
    selected_modes = set()
    while len(selected_modes) < len(Mode):
        m = select_mode(modes)
        selected_modes.update((m,))
