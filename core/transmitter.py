import numpy as np
from .utils import rrc_filter


class Transmitter:
    def __init__(self, sps=16, beta=0.35, span=32, fc=2.0):
        self.sps = sps  # Samples per symbol
        self.beta = beta  # Roll-off factor
        self.span = span  # Filter span
        self.fc = fc  # Carrier frequency
        self.filter_coeff = rrc_filter(sps, beta, span)
        self.phase = 0

    def generate_bits(self, n_bits):
        """Generate random binary sequence"""
        return np.random.randint(0, 2, n_bits)

    def line_encode(self, bits, coding='nrz'):
        """Convert bits to voltage levels"""
        if coding == 'nrz':
            return 2 * bits - 1  # 0-> -1, 1->1
        elif coding == 'manchester':
            # Manchester coding: 0->[1,-1], 1->[-1,1]
            encoded = np.zeros(len(bits) * 2)
            for i, bit in enumerate(bits):
                encoded[2 * i] = 1 if bit == 0 else -1
                encoded[2 * i + 1] = -1 if bit == 0 else 1
            return encoded
        else:
            raise ValueError(f"Unknown coding scheme: {coding}")

    def pulse_shape(self, symbols):
        """Apply RRC pulse shaping"""
        upsampled = np.zeros(len(symbols) * self.sps)
        upsampled[::self.sps] = symbols
        return np.convolve(upsampled, self.filter_coeff, 'same')

    def modulate(self, baseband):
        """BPSK modulation"""
        t = np.arange(len(baseband)) / self.sps
        self.phase = 0  # Conserver la même phase
        carrier = np.cos(2 * np.pi * self.fc * t + self.phase)
        return baseband * carrier