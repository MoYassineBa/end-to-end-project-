# integration_test.py
import numpy as np
from core.transmitter import Transmitter
from core.channel import Channel
from core.receiver import Receiver


def test_full_chain():
    # Initialize components
    tx = Transmitter(sps=16)
    channel = Channel(snr_db=20)
    rx = Receiver(sps=16)

    # Generate test bits
    bits = np.array([0, 1, 0, 1, 1, 0, 1, 0])

    # Transmitter chain
    encoded = tx.line_encode(bits, 'nrz')
    baseband = tx.pulse_shape(encoded)
    modulated = tx.modulate(baseband)

    # Channel
    received = channel.transmit(modulated)

    # Receiver chain (corrected order)
    demodulated = rx.demodulate(received)
    filtered = rx.matched_filter(demodulated)
    samples = rx.clock_recovery(filtered)
    recovered = rx.decision(samples, 'nrz')

    # Calculate BER
    errors = np.sum(bits != recovered)
    ber = errors / len(bits)

    print(f"Original bits: {bits}")
    print(f"Recovered bits: {recovered}")
    print(f"BER: {ber}")

    assert ber == 0.0  # Should be error-free at high SNR


if __name__ == "__main__":
    test_full_chain()