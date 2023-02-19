"""Handles all the processing of audio."""
import json
from pathlib import Path


AUDIO_CACHE = Path(__file__).parent / "audio_cache"


def get_each_note(path: Path) -> list[float]:
    """
    Returns the time of the beginning of each note in a song.

    :param path: The Path object of the sound file.
    """

    filename = str(path).rsplit('/', maxsplit=1)[-1] + ".cache"
    cached_filename = AUDIO_CACHE / filename
    if cached_filename.exists():
        with cached_filename.open() as file:
            times = json.load(file)
            return list(times)

    import librosa

    cached_filename.touch()

    y, sr = librosa.load(path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    beats = librosa.beat.beat_track(y=y, onset_envelope=onset_env, sr=sr, tightness=10.0)[1]
    times = librosa.frames_to_time(beats, sr=sr)

    times = list(times)

    with cached_filename.open("w") as file:
        json.dump(times, file)

    return times
