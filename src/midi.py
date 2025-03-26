# MIDI functions

import io
import pygame

def midi_play(midi:str):
    # Create an in-memory file object from the bytes
    midi_file = io.BytesIO(midi)

    pygame.mixer.init()

    # Load and play the MIDI data
    pygame.mixer.music.load(midi_file)
    pygame.mixer.music.play()

    # Keep the program running while the music plays
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    if True:
        from flashcard import score
        from flashcard import chords
        from flashcard import fcgen

        # play a chord
        note = score.Note("C4")
        ct = chords.ChordType.dom7
        key = score.Key.C
        voicing = chords.Voicing.blues
        (scoreXml, scoreMidi) = fcgen.fc_chord(note, type=ct, voicing=voicing, key=key)
        midi_play(scoreMidi)
