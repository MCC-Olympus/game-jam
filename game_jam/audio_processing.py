"""Handles all the processing of audio."""

import librosa


def get_each_note(path):
    """Returns the time of each note in a song."""
    y, sr = librosa.load(path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    beats = librosa.beat.beat_track(y=y,onset_envelope=onset_env, sr=sr, tightness=10)[1]
    times = librosa.frames_to_time(beats, sr=sr)
    return times