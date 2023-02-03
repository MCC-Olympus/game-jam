"""Handles all the processing of audio."""

import wave

import librosa.display
import pyaudio


def play(path, start, end) -> None:
    # Play a sound file from a given start to end time. Make it echo at the end
    # of the song.
    wf = wave.open(path, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )
    # make it echo and fade out
    for i in range(0, 10):
        wf.setpos(int(start * wf.getframerate()))
        data = wf.readframes(int((end - start) * wf.getframerate()))
        stream.write(data)
        start = end
        end = end + (end - start) * (i + 1) / 10
    stream.stop_stream()
    stream.close()
    p.terminate()


def get_each_note(path):
    """Returns the time of each note in a song."""
    y, sr = librosa.load(path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    return librosa.frames_to_time(beats, sr=sr)
