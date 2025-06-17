import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLabel, QSpinBox, QComboBox, QPushButton)

from core.channel import Channel
from core.receiver import Receiver
from core.transmitter import Transmitter
from .plot_widget import PlotWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Communication Simulator")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Control panel
        control_group = QGroupBox("Simulation Parameters")
        control_layout = QHBoxLayout()

        # Parameter controls
        control_layout.addWidget(QLabel("Number of Bits:"))
        self.bit_spin = QSpinBox()
        self.bit_spin.setRange(10, 1000)
        self.bit_spin.setValue(100)
        control_layout.addWidget(self.bit_spin)

        control_layout.addWidget(QLabel("Coding Scheme:"))
        self.coding_combo = QComboBox()
        self.coding_combo.addItems(["NRZ", "Manchester"])
        control_layout.addWidget(self.coding_combo)

        control_layout.addWidget(QLabel("SNR (dB):"))
        self.snr_spin = QSpinBox()
        self.snr_spin.setRange(-10, 30)
        self.snr_spin.setValue(10)
        control_layout.addWidget(self.snr_spin)

        # Run button
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        control_layout.addWidget(self.run_button)

        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)

        # Plot area
        self.plot_widget = PlotWidget()
        main_layout.addWidget(self.plot_widget)

    def run_simulation(self):
        # Get parameters from UI
        n_bits = self.bit_spin.value()
        coding = self.coding_combo.currentText().lower()
        snr_db = self.snr_spin.value()

        # Run simulation (this would connect to your core logic)
        print(f"Running simulation with {n_bits} bits, {coding} coding, SNR={snr_db}dB")
        # Here you would call your transmitter->channel->receiver chain
        # and update the plot_widget with results

        # Create system components
        sps = 16  # Samples per symbol
        beta = 0.35  # Roll-off factor
        fc = 2.0  # Carrier frequency (normalized)

        tx = Transmitter(sps=sps, beta=beta, fc=fc)
        channel = Channel(snr_db=snr_db)
        rx = Receiver(sps=sps, beta=beta, fc=fc)

        # 1. Generate binary sequence
        original_bits = tx.generate_bits(n_bits)

        # 2. Transmitter processing
        encoded = tx.line_encode(original_bits, coding)
        shaped = tx.pulse_shape(encoded)
        modulated = tx.modulate(shaped)

        # 3. Channel transmission
        received = channel.transmit(modulated)

        # 4. Receiver processing (corrected order)
        demodulated = rx.demodulate(received)
        filtered = rx.matched_filter(demodulated)
        samples = rx.clock_recovery(filtered)
        recovered_bits = rx.decision(samples, coding)

        # 5. Calculate BER
        min_length = min(len(original_bits), len(recovered_bits))
        errors = np.sum(original_bits[:min_length] != recovered_bits[:min_length])
        ber = errors / min_length if min_length > 0 else 0

        # 6. Update status bar
        self.statusBar().showMessage(
            f"Simulation complete. BER: {ber:.4f} ({errors}/{min_length} errors) | "
            f"Bits: {n_bits}, Coding: {coding}, SNR: {snr_db}dB"
        )

        # 7. Update plots
        self.plot_widget.update_plots(
            original_bits,
            modulated,
            received,
            recovered_bits
        )

        # 8. (Optional) Save simulation data for analysis
        self.last_simulation = {
            'original_bits': original_bits,
            'modulated': modulated,
            'received': received,
            'recovered_bits': recovered_bits,
            'params': {
                'n_bits': n_bits,
                'coding': coding,
                'snr_db': snr_db,
                'sps': sps,
                'ber': ber
            }
        }

        print(f" last simulation : {self.last_simulation}")