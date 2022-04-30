import numpy as np
import math


class GenerateSignal:
    def __init__(self, freq_sampling: float, time_measured: float) -> dict:

        self.freq_sampling = freq_sampling
        self.time_measured = time_measured
        self.samplings = round(freq_sampling * time_measured)
        self.vector_time = np.linspace(0, time_measured, int(self.samplings))

    def generate_senoidal_signal(
        self, frequency: float, signal_amplitude: float
    ) -> dict:

        angular_frequency = 2 * math.pi * frequency

        return {
            "time": list(self.vector_time),
            "signal": list(
                signal_amplitude * np.sin(angular_frequency * self.vector_time)
            ),
        }

    def generate_noise_signal(self, noise_amplitude: float) -> dict:

        return {
            "time": list(self.vector_time),
            "signal": list(noise_amplitude * np.random.rand(self.samplings)),
        }

    def generate_senoidal_noise_signal(
        self, frequency: float, signal_amplitude: float, noise_amplitude: float
    ) -> dict:

        signal = self.generate_senoidal_signal(frequency, signal_amplitude).get(
            "signal"
        )

        noise = self.generate_noise_signal(noise_amplitude).get("signal")
        
        return {"time": list(self.vector_time), "signal": list(np.array(signal) + np.array(noise))}
