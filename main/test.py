import numpy as np
import pyaudio
import threading
from tkinter import *
import math
import scipy.signal as sig


class GUI(Tk):
    def __init__(self):
        super(GUI, self).__init__()
        self.title = "Slider"
        self.scale = Scale(self, from_=0, to=825, length=825, orient=HORIZONTAL)
        self.scale.pack()
        self.scale2 = Scale(self, from_=0, to=100, length=100, orient=VERTICAL)
        self.scale2.pack()

    def read_scale(self):
        return self.scale.get()

    def read_volume(self):
        return self.scale2.get()


class SoundGenerator:
    def __init__(self):
        self.frequency = 0
        self.sample_rate = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.sample_rate,
                                  frames_per_buffer=1024,
                                  output=True)

    @staticmethod
    def note_to_frequency(n):
        return 55 * pow(2, n / 12)

    def set_frequency(self, notes_from_A1):
        self.frequency = self.note_to_frequency(notes_from_A1)

    @staticmethod
    def triangle_wave(phase):
        net_phase = (phase % (2 * np.pi)) / (2 * np.pi)
        if net_phase <= 0.5:
            return net_phase
        elif net_phase > 0.5:
            return 1 - net_phase

    @staticmethod
    def piano_wave(phase):
        return -1 / 4 * np.sin(3 * phase) + 1 / 4 * np.sin(1 * phase) + math.sqrt(3) / 2 * np.cos(1 * phase)

    def complex_wave(self, phase):
        return pow(self.piano_wave(phase), 3)

    def wave_form(self, phase, form):
        if form == "sin":
            return np.sin(phase)
        elif form == "triangle":
            return self.triangle_wave(phase)
        # TODO: fix
        elif form == "sawtooth":
            return sig.sawtooth(phase % (2 * np.pi))
        elif form == "piano":
            return self.piano_wave(phase)
        elif form == "complex":
            return self.complex_wave(phase)

    def loop(self):
        # CHANGE SETTINGS
        x = 0
        m_phase = 0
        sensitivity = 1
        form = "sin"

        while True:
            global notes, amplitude
            self.set_frequency(notes_from_A1=notes)
            signal = []
            phaseInc = 2 * np.pi * self.frequency / self.sample_rate
            for i in range(sensitivity):
                signal.append(amplitude * self.wave_form(m_phase, form))
                m_phase += phaseInc

            signal = np.array(signal).astype(np.float32)

            self.stream.write(signal.tobytes())
            x += 1

    def run(self):
        t1 = threading.Thread(target=self.loop)
        t1.start()


gui = GUI()

notes = 0
amplitude = 0


class Loop(threading.Thread):
    def run(self):
        while True:
            global notes, amplitude
            notes = gui.read_scale() / 13.75
            amplitude = gui.read_volume() / 100


s = SoundGenerator()
s.run()
loop = Loop()
loop.start()

gui.mainloop()
