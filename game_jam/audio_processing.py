"""Handles all the processing of audio."""

import librosa
import numpy as np


def get_each_note(path):
    """Returns the time of each note in a song and the frequency at that time."""
    y, sr = librosa.load(path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)[1]

    times = librosa.frames_to_time(beats, sr=sr)
    return times, get_frequencies(path, times)


def get_frequencies(filename, time_stamps) -> list[float]:
    """Gets the average frequency of each note."""
    # Load the audio samples
    samples, sr = librosa.load(filename)

    avg_frequencies = []
    for time in time_stamps:
        # Extract a segment of the audio
        start = time * sr
        end = start + sr
        segment = samples[int(start) : int(end)]

        # Convert the audio to the frequency domain
        spectrum = np.abs(np.fft.rfft(segment))

        # Calculate the average frequency
        avg_frequency = np.mean(spectrum)

        # Add the average frequency to the list
        avg_frequencies.append(avg_frequency)

    # Make the list of floats
    return [float(frequency) for frequency in avg_frequencies]
