import numpy as np
from .utils import awgn


class Channel:
    def __init__(self, snr_db=10.0):
        self.snr_db = snr_db

    def transmit(self, signal):
        """Add AWGN noise to signal"""
        return awgn(signal, self.snr_db)