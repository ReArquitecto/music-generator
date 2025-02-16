# flash-card generators

import random
import os
import shutil
from score import *

circle = {'C', 'G', 'D', 'A', 'E', 'B', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'} # -- maybe soon

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
    n2 = Note(n1.midi() + interval)
    tick = Tick(Duration(1), {n1, n2})
    seq = Sequence(clef, [tick])
    score = Score({seq}, keyAndMode=keyAndMode)
    score.write(fname)

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
        # FIXME: some strange cases appear, like F# for Gb major.  Not yet sure what the best approach might be.
        # Consider using accidentlByStep: https://www.music21.org/music21docs/usersGuide/usersGuide_15_key.html#example-adjusting-notes-to-fit-the-key-signature
        keys = {Key.C, Key.D, Key.E, Key.F, Key.G, Key.A, Key.B, Key.Bflat, Key.Eflat, Key.Aflat, Key.Dflat, Key.Gflat}
        modes = {Mode.ionian, Mode.dorian, Mode.phrygian, Mode.lydian, Mode.mixolydian, Mode.aeolian, Mode.locrian}
        modes = {Mode.major} # keep it simple ... any mode works but this way it's easier to see if it makes sense
        kam = KeyAndMode(select_key(keys), select_mode(modes))
        print(kam)
        fc_randnote("output/fcgen-key.xml", NoteRange(Note("A4"), Note("G#5")), keyAndMode=kam)
        web.display_musicxml("fcgen-key", "output/fcgen-key.html", "output/fcgen-key.xml", description=str(kam))


    # Generate a suite of flashcards
    mkdirs("") # clear the decks (deletes xml and html dirs)

    # single note
    if True:
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
    
    # Intervals

    intervals = (
        (3, "minor3rd"),
        (4, "3rd"),
        (5, "4th"),
        (6, "flat5th"),
        (7, "5th"),
        (9, "6th"),
        (12, "octave")
    )

    for interval in intervals:    
        dir = f"intervals/{interval[1]}/keysig-C"
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
            dir = f"intervals/{interval[1]}/keysig-" + k
            htmldir, xmldir = mkdirs(dir)
            for nn in range(36, 84):
                n = Note(nn, keyAndMode=kam)
                notename = n.name
                html_fname = f"{htmldir}/{notename}.html"
                xml_fname = f"{xmldir}/{notename}.xml"
                fc_interval(xml_fname, Note(notename), interval[0], keyAndMode=kam)
                web.gen_musichtml(xml_fname, html_fname, xml_fname)

        

