# flash-card generators

import random
import os
import shutil

from score import *
from chords import *

circle = {'C', 'G', 'D', 'A', 'E', 'B', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'}

class NoteRange(object):
    def __init__(self, low:Note, high:Note):
        self.low = low
        self.high = high

    def __str__(self):
        return "NoteRange(%d, %d)" % (self.low, self.high)

def random_note(range:NoteRange, keyAndMode:KeyAndMode=None):
    '''Generate a random Note within the given range'''
    low = range.low.midi()
    high = range.high.midi()
    chosen = random.randint(low, high)
    return Note(chosen, keyAndMode)

def fc_randnote(fname:str, range:NoteRange, clef:Clef=None, keyAndMode:KeyAndMode=None):
    note = random_note(range, keyAndMode)
    tick = Tick(Duration(1), {note})
    seq = Sequence(clef, [tick])
    score = Score({seq}, keyAndMode=keyAndMode)
    score.write(fname)

def fc_notes(fname:str, notes:set[Note], clef:Clef=None, keyAndMode:KeyAndMode=None):
    tick = Tick(Duration(1), notes)
    seq = Sequence(clef, [tick])
    score = Score({seq}, keyAndMode=keyAndMode)
    score.write(fname)

def fc_interval(fname:str, n1:Note, interval:int, clef:Clef=None, keyAndMode:KeyAndMode=None):
    '''Create a flashcard with a random note and another note at the given interval above'''
    n2 = Note(n1.note.pitch.transpose(interval))
    tick = Tick(Duration(1), {n1, n2})
    seq = Sequence(clef, [tick])
    score = Score({seq}, keyAndMode=keyAndMode)
    score.write(fname)

def fc_chord(fname:str, n1:Note, type:ChordType, voicing:Voicing, key: Key):
    ch = Chord(type, voicing)
    parts = chord(n1, key, ch.parts)
    # parts is a list of parts, where a part is a list of notes.
    if parts is None:
        return None
    seqs = []
    for part in parts:
        tick = Tick(Duration(1), part)
        # treble part is first (or only)
        if len(seqs) == 0:
            clef = Clef.Treble
        else:
            clef = Clef.Bass
        seq = Sequence(clef, [tick])
        seqs.append(seq)
    score = Score(seqs, keyAndMode=KeyAndMode(key, Mode.major))
    score.write(fname)
    return score

def select_key(key:set[Key]):
    '''Select a random key from the given set'''
    return random.choice(list(key))

def select_mode(mode:set[Mode]):
    '''Select a random mode from the given set'''
    return random.choice(list(mode))

def mkdir(dir:str):
    shutil.rmtree(dir, ignore_errors=True)
    try:
        os.makedirs(dir)
    except FileExistsError:
        pass

def mkdirs(dir:str):
    htmldir = f"output/html/{dir}"
    xmldir = f"output/xml/{dir}"
    mkdir(htmldir)
    mkdir(xmldir)
    return htmldir, xmldir

def gen_singles():
    ''' generate single note flashcards'''
    dir = "single/keysig-C"
    htmldir, xmldir = mkdirs(dir)
    for octave in ("2", "3", "4", "5", "6"):
        for n in Key:
            notename = n.name + octave
            html_fname = f"{htmldir}/{notename}.html"
            xml_fname = f"{xmldir}/{notename}.xml"
            fc_notes(xml_fname, {Note(notename)})
            web.gen_musichtml(xml_fname, html_fname, xml_fname)

    for k in circle:
        if k == 'C':
            continue # already handled above
        kam = KeyAndMode(Key(k), Mode.major)
        dir = "single/keysig-" + k
        htmldir, xmldir = mkdirs(dir)
        for nn in range(36, 84):
            n = Note(nn, keyAndMode=kam)
            notename = n.name
            html_fname = f"{htmldir}/{notename}.html"
            xml_fname = f"{xmldir}/{notename}.xml"
            fc_notes(xml_fname, {Note(notename)}, keyAndMode=kam)
            web.gen_musichtml(xml_fname, html_fname, xml_fname)

def gen_intervals():
    intervals = (
        ('m3', 'minor3rd'),
        ('M3', '3rd'),
        ('P4', '4th'),
        ('d5', 'flat5th'),
        ('P5', '5th'),
        ('M6', '6th'),
        ('P8', 'octave')
    )

    for interval in intervals:    
        dir = f"intervals/keysig-C/{interval[1]}"
        htmldir, xmldir = mkdirs(dir)
        for octave in ("2", "3", "4", "5", "6"):
            for n in Key:
                notename = n.name + octave
                html_fname = f"{htmldir}/{notename}.html"
                xml_fname = f"{xmldir}/{notename}.xml"
                fc_interval(xml_fname, Note(notename), interval[0])
                web.gen_musichtml(xml_fname, html_fname, xml_fname)
        
        for k in circle:
            if k == 'C':
                continue # already handled above
            kam = KeyAndMode(Key(k), Mode.major)
            dir = f"intervals/keysig-{k}/{interval[1]}"
            htmldir, xmldir = mkdirs(dir)
            for nn in range(36, 84):
                n = Note(nn, keyAndMode=kam)
                notename = n.name
                html_fname = f"{htmldir}/{notename}.html"
                xml_fname = f"{xmldir}/{notename}.xml"
                fc_interval(xml_fname, Note(notename), interval[0], keyAndMode=kam)
                web.gen_musichtml(xml_fname, html_fname, xml_fname)

def gen_chords():
    mkdirs("chords")
    octave = '4'
    for keysig in circle:
        key = Key(keysig)
        for voicing in Voicing:
            for type in ChordType:
                found = False
                dir = f"chords/keysig-{keysig}/{voicing.name}/{type.name}"
                htmldir, xmldir = mkdirs(dir)
                for k in circle:
                    notename = k + octave
                    note = Note(notename)
                    html_fname = f"{htmldir}/{k}{type.name}.html"
                    xml_fname = f"{xmldir}/{k}{type.name}.xml"
                    score = fc_chord(xml_fname, note, type, voicing, key)
                    if score is None:
                        continue
                    found = True
                    web.gen_musichtml("fcgen-chord", html_fname, xml_fname, description=f"{k}{type.value} {voicing.name} voicing in {keysig}")
                if not found:
                    os.rmdir(htmldir)
                    os.rmdir(xmldir)

if __name__ == "__main__":
    import web

    if False:
        # print a random note
        print("Random note: " + str(random_note(NoteRange(Note("C4"), Note("G4")))))

        # Generate flash cards, each with a random note

        # Note: in the following, the notes are above bass clef to show that bass clef is forced
        fc_randnote("output/fcgen-note-bass.xml", NoteRange(Note("C#4"), Note("G4")), Clef.Bass)
        web.display_musicxml("fcgen-note-bass", "output/fcgen-note-bass.html", "output/fcgen-note-bass.xml")

        # Note that this is not the note printed above
        fc_randnote("output/fcgen-note.xml", NoteRange(Note("C4"), Note("G4")))
        web.display_musicxml("fcgen-note", "output/fcgen-note.html", "output/fcgen-note.xml")

    if False:
        # select random key and mode
        keys = {Key.C, Key.D, Key.E, Key.F, Key.G, Key.A, Key.B, Key.Bflat, Key.Eflat, Key.Aflat, Key.Dflat, Key.Gflat}
        modes = {Mode.ionian, Mode.dorian, Mode.phrygian, Mode.lydian, Mode.mixolydian, Mode.aeolian, Mode.locrian}
        modes = {Mode.major} # keep it simple ... any mode works but this way it's easier to see if it makes sense
        kam = KeyAndMode(select_key(keys), select_mode(modes))
        print(kam)
        fc_randnote("output/fcgen-key.xml", NoteRange(Note("A4"), Note("G#5")), keyAndMode=kam)
        web.display_musicxml("fcgen-key", "output/fcgen-key.html", "output/fcgen-key.xml", description=str(kam))


    if True:
        # Generate a suite of flashcards
        # mkdirs("") # clear the decks (empties xml and html dirs)
        gen_singles()
        gen_intervals()
        gen_chords()

        print(f"{web.file_count} flashcards generated")
