import numpy as np
from .utils import rrc_filter


class Receiver:
    def __init__(self, sps=16, beta=0.35, span=32, fc=2.0):
        self.sps = sps
        self.beta = beta
        self.span = span
        self.fc = fc
        self.filter_coeff = rrc_filter(sps, beta, span)

    def demodulate(self, signal):
        """BPSK demodulation"""
        t = np.arange(len(signal)) / self.sps
        carrier = np.cos(2 * np.pi * self.fc * t)
        return signal * carrier

    def matched_filter(self, signal):
        """Apply matched RRC filter"""
        return np.convolve(signal, self.filter_coeff, 'same')

    def clock_recovery(self, signal, method='peak'):
        """Symbol timing recovery"""
        if method == 'peak':
            # Simple peak detection (for testing)
            peaks = np.abs(signal)
            return signal[np.argmax(peaks) % self.sps:: self.sps]
        else:
            # Advanced method would go here
            return signal[self.sps // 2:: self.sps]

    def decision(self, samples, coding='nrz'):
        """Threshold detection"""
        if coding == 'nrz':
            return (samples > 0).astype(int)
        elif coding == 'manchester':
            # Decode Manchester
            bits = np.zeros(len(samples) // 2)
            for i in range(len(bits)):
                if samples[2 * i] > 0 and samples[2 * i + 1] < 0:
                    bits[i] = 0
                elif samples[2 * i] < 0 and samples[2 * i + 1] > 0:
                    bits[i] = 1
            return bits