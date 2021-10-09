import librosa
import numpy

class Analyser:
    def __init__(self, time_series, sample_rate):
        hop_length = 512
        n_fft = 2048 * 4
        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = numpy.abs(librosa.stft(time_series, hop_length=hop_length, n_fft=n_fft))
        self.spectrogram = librosa.amplitude_to_db(stft, ref=numpy.max)  # converting the matrix to decibel matrix
        frequencies = librosa.core.fft_frequencies(n_fft)  # getting an array of frequencies

        # getting an array of time periodic
        times = librosa.core.frames_to_time(
            numpy.arange(self.spectrogram.shape[1]),
            sr=sample_rate,
            hop_length=512,
            n_fft=n_fft
        )

        self.timeIndexRatio = len(times) / times[len(times) - 1]
        self.frequenciesIndexRatio = len(frequencies) / frequencies[len(frequencies) - 1]

    def get_decibel(self, targetTime, frequency):
        return self.spectrogram[int(frequency * self.frequenciesIndexRatio)][int(targetTime * self.timeIndexRatio)]
