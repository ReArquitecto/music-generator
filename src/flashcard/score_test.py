
from flashcard.score import *

def test_KeyAndMode():
    kam = KeyAndMode(Key('C'), mode=Mode.major)
    assert kam.name == "C major"
