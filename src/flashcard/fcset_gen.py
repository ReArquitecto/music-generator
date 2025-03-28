# generate sets of flashcards

import shutil
import os

from flashcard.score import *
from flashcard.chords import *
from flashcard.fcgen import *

deleteDirs = True

def mkdir(dir:str):
    if deleteDirs:
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

def fcset_write(scoreXml:str, title:str, html_filename:str, xml_filename:str, description=None):
    # ignore scores with double-sharp or flat-flat accidentals
    # TODO: use RE as it's faster
    if "<accidental>double-sharp</accidental>" in scoreXml:
        return
    if "<accidental>flat-flat</accidental>" in scoreXml:
        return
    with open(xml_filename, "w") as f:
        f.write(scoreXml)
    web.gen_musichtml(title, html_filename, xml_filename, description)

def gen_singles():
    ''' generate single note flashcards'''
    dir = "single/keysig-C"
    htmldir, xmldir = mkdirs(dir)
    print(f"generating singles in {dir}")
    for octave in ("2", "3", "4", "5", "6"):
        for n in Key:
            notename = n.name + octave
            html_fname = f"{htmldir}/{notename}.html"
            xml_fname = f"{xmldir}/{notename}.xml"
            (scoreXml, scoreMidi) = fc_notes((Note(notename),))
            fcset_write(scoreXml, xml_fname, html_fname, xml_fname)

    for k in circle:
        if k == 'C':
            continue # already handled above
        kam = KeyAndMode(Key(k), Mode.major)
        dir = "single/keysig-" + k
        print(f"generating singles in {dir}")
        htmldir, xmldir = mkdirs(dir)
        for nn in range(36, 84):
            n = Note(nn, keyAndMode=kam)
            notename = n.name
            html_fname = f"{htmldir}/{notename}.html"
            xml_fname = f"{xmldir}/{notename}.xml"
            (scoreXml, scoreMidi) = fc_notes({Note(notename)}, keyAndMode=kam)
            fcset_write(scoreXml, xml_fname, html_fname, xml_fname)

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
        print(f"generating {interval[1]} intervals")
        dir = f"intervals/keysig-C/{interval[1]}"
        htmldir, xmldir = mkdirs(dir)
        for octave in ("2", "3", "4", "5", "6"):
            for n in Key:
                notename = n.name + octave
                html_fname = f"{htmldir}/{notename}.html"
                xml_fname = f"{xmldir}/{notename}.xml"
                (scoreXml, scoreMidi) = fc_interval(Note(notename), interval[0])
                fcset_write(scoreXml, xml_fname, html_fname, xml_fname)
        
        for k in root_notes:
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
                (scoreXml, scoreMidi) = fc_interval(Note(notename), interval[0], keyAndMode=kam)
                fcset_write(scoreXml, xml_fname, html_fname, xml_fname)

def gen_chords():
    mkdirs("chords")
    octave = '4'
    for keysig in circle:
        print(f"generating chords in {keysig}")
        key = Key(keysig)
        for voicing in Voicing:
            for ctype in ChordType:
                found = False
                dir = f"chords/keysig-{keysig}/{voicing.name}/{ctype.name}"
                htmldir, xmldir = mkdirs(dir)
                for k in root_notes:
                    notename = k + octave
                    note = Note(notename)
                    html_fname = f"{htmldir}/{k}{ctype.name}.html"
                    xml_fname = f"{xmldir}/{k}{ctype.name}.xml"
                    outputs = fc_chord(note, ctype, voicing, key)
                    if outputs is None:
                        continue
                    (scoreXml, scoreMidi) = outputs
                    found = True
                    fcset_write(scoreXml, "fcset-chord", html_fname, xml_fname, description=f"{k}{ctype.value} {voicing.name} voicing in {keysig}")
                if not found:
                    os.rmdir(htmldir)
                    os.rmdir(xmldir)

if __name__ == "__main__":
    import web

    # Generate a suite of flashcards

    # deleteDirs = False # TEMP: don't delete all files first (don't check in uncommented)
    mkdirs("") # clear the decks (empties xml and html dirs if they exist)

    gen_singles()
    gen_intervals()
    gen_chords()

    print(f"{web.file_count} flashcards generated")
