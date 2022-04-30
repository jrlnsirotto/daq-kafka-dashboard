from signal.signal_generator import GenerateSignal
from confluent_kafka import Producer
import socket, json, traceback, time, pandas as pd


def acked(err, msg):
    if err is not None:
        print(
            f"Failed to deliver message at: {pd.Timestamp.now()}. Traceback:{traceback.format_exc()}"
        )
    else:
        print(f"Message produced at: {pd.Timestamp.now()}")


conf = {
    "bootstrap.servers": "0.0.0.0:29092,:::29092",
    "client.id": socket.gethostname(),
}

producer = Producer(conf)

while True:
    parameters = json.load(open("signal/producer_parameters.json"))
    measuring_status = parameters.get("measuring", False)
    sig = GenerateSignal(
        parameters.get("freq_sampling"), parameters.get("time_measured")
    )
    if measuring_status:
        noise_senoidal_signal = sig.generate_senoidal_noise_signal(
            parameters.get("senoidal_frequency"),
            parameters.get("senoidal_amplitude"),
            parameters.get("noise_amplitude"),
        )
        message = json.dumps(noise_senoidal_signal, indent=4)

        producer.produce(
            "sensor-signal",
            value=message,
            callback=acked,
        )
        time.sleep(5 * parameters.get("time_measured"))

    # Wait up to 1 second for events. Callbacks will be invoked during
    # this method call if the message is acknowledged.
    producer.poll(5)
