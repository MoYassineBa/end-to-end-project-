import numpy as np
from scipy import signal

def rrc_filter(sps, beta, span):
    """Root Raised Cosine filter"""
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    h = np.zeros_like(t)
    for i, ti in enumerate(t):
        if ti == 0:
            h[i] = 1.0 - beta + 4*beta/np.pi
        elif abs(ti) == 1/(4*beta):
            h[i] = (beta/np.sqrt(2)) * ((1+2/np.pi)*np.sin(np.pi/(4*beta)) +
                     (1-2/np.pi)*np.cos(np.pi/(4*beta)))
        else:
            h[i] = (np.sin(np.pi*ti*(1-beta)) +
                    4*beta*ti*np.cos(np.pi*ti*(1+beta))) / \
                    (np.pi*ti*(1-(4*beta*ti)**2))
    return h / np.sqrt(np.sum(h**2))


def awgn(signal, snr_db):
    """Add AWGN noise"""
    snr_linear = 10**(snr_db/10.0)
    power = np.mean(np.abs(signal)**2)
    noise_power = power / snr_linear
    noise = np.random.normal(0, np.sqrt(noise_power/2), len(signal)) + \
            1j*np.random.normal(0, np.sqrt(noise_power/2), len(signal))
    return signal + noise