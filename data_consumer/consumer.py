from confluent_kafka import Consumer
import json, sys, os, pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from data_storage import manipulate_hdf5


conf = {
    "bootstrap.servers": "0.0.0.0:29092,:::29092",
    "group.id": "sensor-signal",
    "auto.offset.reset": "smallest",
}

consumer = Consumer(conf)

running = True

topics = ["sensor-signal"]


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=10.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    raise KafkaException(msg.error())
            else:

                message_value = json.loads(msg.value())

                manipulate_hdf5.dataset_insert(
                    "measurements",
                    "periodic_signal_group",
                    f"{str(pd.Timestamp.now())}",
                    [message_value.get("time"), message_value.get("signal")],
                )

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    running = False


basic_consume_loop(consumer, topics)
