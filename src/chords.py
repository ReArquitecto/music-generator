# chord dictionary

from enum import Enum

# see https://en.wikipedia.org/wiki/Chord_(music) -- not all are here
# The goal isn't to produce all possible chords, but to cover the main ones.

class ChordType(Enum):
    # triads
    maj = "maj"
    min = "min"
    dim = "dim"
    aug = "aug"

    # 7ths
    maj7 = "maj7"
    min7 = "min7"
    dom7 = "7"
    hdim = "min7b5" # aka half-diminished
    dim7 = "dim7"

    # 9ths
    maj9 = "maj9"
    min9 = "min9"
    dom9 = "9"
    dom7b9 = "7b9"
    dom7s9 = "7#9"

    # 11ths
    eleventh = "11" # omit 3rd
    dom11 = "dom11" # major 3 minor 7
    min11 = "min11" # minor 3 minor 7
    maj11 = "maj11" # major 3 major 7

    # 13ths
    dom13 = "13"

    alt = "alt" # need a section on these, see https://en.wikipedia.org/wiki/Altered_chord


def standard_voicing(type=ChordType):
    match type:
        case ChordType.maj: return (('P1', 'M3', 'P5'),)
        case ChordType.min: return (('P1', 'm3', 'P5'),)
        case ChordType.dim: return (('P1', 'm3', 'd5'),)
        case ChordType.aug: return (('P1', 'M3', 'A5'),)
        case ChordType.maj7: return (('P1', 'M3', 'P5', 'M7'),)
        case ChordType.min7: return (('P1', 'm3', 'P5', 'm7'),)
        case ChordType.dom7: return (('P1', 'm3', 'P5', 'M7'),)
        case ChordType.hdim: return (('P1', 'm3', 'd5', 'm7'),)
        case ChordType.dim7: return (('P1', 'm3', 'd5', 'd7'),)
        case ChordType.maj9: return (('P1', 'M3', 'P5', 'M7', 'M9'),)
        case ChordType.min9: return (('P1', 'm3', 'P5', 'M7', 'M9'),)
        case ChordType.dom9: return (('P1', 'M3', 'P5', 'm7', 'M9'),)
        case ChordType.dom7b9: return (('P1', 'M3', 'P5', 'm7', 'm9'),)
        case ChordType.dom7s9: return (('P1', 'M3', 'P5', 'm7', 'a9'),)
        case ChordType.eleventh: return (('P1', 'P5', 'm7', 'M9', 'P11'),)
        case ChordType.dom11: return (('P1', 'M3', 'P5', 'm7', 'M9', 'P11'),)
        case ChordType.min11: return (('P1', 'm3', 'P5', 'm7', 'M9', 'P11'),)
        case ChordType.maj11: return (('P1', 'M3', 'P5', 'M7', 'M9', 'P11'),)
        case ChordType.dom13: return (('P1', 'M3', 'P5', 'm7', 'M9', 'P11', 'M13'),)
        case ChordType.alt: return (('P1', 'M3', 'A5', 'm7', 'm9', 'A9'),)
    return None

# The two "blues" voicings are common useful voicings Jeff added, as examples
# of how to use ChordType, and also potentially useful flashcards.
# More useful voicings can be found at
# https://www.thejazzpianosite.com/jazz-piano-lessons/jazz-chord-voicings/

def blues_voicing(type=ChordType):
    match type:
        case ChordType.maj: return (('-P8',), ('P1', 'M3', 'P5'))
        case ChordType.min: return (('-P8',), ('P1', 'm3', 'P5'))
        case ChordType.dim: return (('-P8',), ('P1', 'm3', 'd5'))
        case ChordType.aug: return (('-P8',), ('P1', 'M3', 'A5'))
        case ChordType.maj7: return (('-P8',), (-1, 'M3', 'P5'))
        case ChordType.min7: return (('-P8',), (-2, 'm3', 'P5'))
        case ChordType.dom7: return (('-P8',), (-2, 'M3', 'P5'))
        case ChordType.hdim: return None
        case ChordType.dim7: return (('-P8',), (-3, 'm3', 'd5'))

        case ChordType.maj9: return (('-P8',), ('M3', 'M7', 'M9'))
        case ChordType.min9: return (('-P8',), ('m3', 'm7', 'M9'))
        case ChordType.dom9: return (('-P8',), ('m3', 'M7', 'M9'))
        case ChordType.dom7b9: return (('-P8',), ('M3', 'm7', 'm9'))
        case ChordType.dom7s9: return (('-P8',), ('M3', 'm7', 'a9'))

        case ChordType.eleventh: return (('-P8',), ('P5', 'm7', 'M9', 'P11'))
        case ChordType.dom11: return None
        case ChordType.min11: return (('-P8',), ('P5', 'm7', 'M9', 'm10', 'P11'))
        case ChordType.maj11: return None
        case ChordType.dom13: return (('-P8',), (-2, 'M3', 'M6'))
        case ChordType.alt: return (('-P8',), ('M3', 'A5', 'm7', 'm9', 'A9'))
    return None

def blues_tight_voicing(type=ChordType):
    match type:
        case ChordType.maj9: return (('-P8',), (-1, 'M2', 'M3', 'P5'))
        case ChordType.min9: return (('-P8',), (-2, 'M2', 'm3', 'P5'))
        case ChordType.dom9: return (('-P8',), (-2, 'M2', 'M3', 'P5'))
        case ChordType.dom7b9: return (('-P8',), (-2, 'm2', 'M3', 'P5'))
    return None

class Voicing(Enum):
    standard = standard_voicing,        # 1, 3, 5, ...
    blues = blues_voicing,              # root plus triad
    blues_tight = blues_tight_voicing,  # root plus tighter triad
    # More coming, see https://www.thejazzpianosite.com/jazz-piano-lessons/jazz-chord-voicings/

class Chord(object):
    def __init__(self, type=ChordType, voicing:Voicing=Voicing.standard):
        self.parts = voicing.value[0](type)
        pass
        return
        match voicing:
            case Voicing.blues:
                self.parts = blues_voicing(type)
            case _:
                self.parts = standard_voicing(type)
