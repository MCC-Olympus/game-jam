"""Handles all the processing of audio."""
import json
from pathlib import Path


AUDIO_CACHE = Path(__file__).parent / "audio_cache"


def get_each_note(path):
    """Returns the time of each note in a song."""

    fname = str(path).split("/")[-1] + ".cache"
    cfname = AUDIO_CACHE / fname
    if cfname.exists():
        with cfname.open() as file:
            times = json.load(file)
            return list(times)

    import librosa

    cfname.touch()

    y, sr = librosa.load(path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    beats = librosa.beat.beat_track(y=y, onset_envelope=onset_env, sr=sr, tightness=10)[1]
    times = librosa.frames_to_time(beats, sr=sr)

    times = list(times)

    with cfname.open("w") as file:
        json.dump(times, file)

    return times