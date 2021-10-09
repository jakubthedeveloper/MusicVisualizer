class Modifier:
    def __init__(self, analyser):
        self.frequencies = [100, 800, 2000, 8000]
        self.values = [0, 0, 0, 0]
        self.weights = [0.01, 0.01, 0.01, 0.01]
        self.analyser = analyser

    def update(self, pos):
        for i, frequency in enumerate(self.frequencies):
            decibel = self.analyser.get_decibel(pos, frequency)
            self.values[i] = abs(decibel) * self.weights[i]
