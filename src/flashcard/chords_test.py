import pytest

from flashcard import chords

def test_chords_all():
    # exercise all voicings for all chord types
    for voicing in chords.Voicing:
        for ch_type in chords.ChordType:
            ch = chords.Chord(ch_type, voicing)

def test_chords_nones():
    for voicing in chords.Voicing:
        ch = chords.Chord(None, voicing)
        assert ch.parts == None, f"expected parts==None for unmapped chord type for {voicing} voicing"
