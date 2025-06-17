import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)

        # Create subplots
        self.ax1 = self.figure.add_subplot(411)
        self.ax2 = self.figure.add_subplot(412)
        self.ax3 = self.figure.add_subplot(413)
        self.ax4 = self.figure.add_subplot(414)

        # Set titles
        self.ax1.set_title("Original Bits")
        self.ax2.set_title("Transmitted Signal")
        self.ax3.set_title("Received Signal")
        self.ax4.set_title("Recovered Bits")

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_plots(self, original_bits, tx_signal, rx_signal, recovered_bits):
        """Update all plots with new data"""
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        # Plot 1: Original Bits
        self.ax1.stem(original_bits[:50], linefmt='b-', markerfmt='bo', basefmt=' ')
        self.ax1.set_title(f"Original Bits (First 50)")
        self.ax1.set_ylim(-0.1, 1.1)
        self.ax1.grid(True)

        # Plot 2: Transmitted Signal
        samples_to_show = min(200, len(tx_signal))
        t = np.arange(samples_to_show) / 16  # Time axis (sps=16)
        self.ax2.plot(t, np.real(tx_signal[:samples_to_show]), 'b')
        self.ax2.set_title("Transmitted Signal (First 200 samples)")
        self.ax2.set_xlabel("Symbol Periods")
        self.ax2.grid(True)

        # Plot 3: Received Signal
        self.ax3.plot(t, np.real(rx_signal[:samples_to_show]), 'r')
        self.ax3.set_title("Received Signal (With Noise)")
        self.ax3.set_xlabel("Symbol Periods")
        self.ax3.grid(True)

        # Plot 4: Recovered Bits
        self.ax4.stem(recovered_bits[:50], linefmt='g-', markerfmt='go', basefmt=' ')
        self.ax4.set_title(f"Recovered Bits (First 50)")
        self.ax4.set_ylim(-0.1, 1.1)
        self.ax4.grid(True)

        # Add BER annotation to recovered bits plot
        min_length = min(len(original_bits), len(recovered_bits))
        errors = np.sum(original_bits[:min_length] != recovered_bits[:min_length])
        ber = errors / min_length if min_length > 0 else 0
        self.ax4.annotate(f"BER: {ber:.4f} ({errors}/{min_length} errors)",
                          xy=(0.05, 0.95), xycoords='axes fraction',
                          bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

        # Adjust layout and redraw
        self.figure.tight_layout()
        self.canvas.draw()