from fastapi import FastAPI
import json
import pandas as pd
from pydantic import BaseModel
from data_storage import manipulate_hdf5

app = FastAPI()


@app.get("/alive")
def alive_check():
    return {"message": "Hello, I'm here and working!"}


@app.get("/daq/parameters")
def read_item():
    parameters = json.load(open("data_producer/signal/producer_parameters.json"))
    return parameters


@app.get("/daq/start")
def start_measurement():

    file = "data_producer/signal/producer_parameters.json"

    parameters = json.load(open(file))

    new_parameters = (True, str(pd.Timestamp.now()), "Started measurement")

    parameters.update(
        dict(zip(["measuring", "last_updated", "updated_action"], new_parameters))
    )

    with open(file, "w") as json_file:
        json.dump(parameters, json_file)

    return parameters


@app.get("/daq/finish")
def finish_measurement():

    file = "data_producer/signal/producer_parameters.json"

    parameters = json.load(open(file))

    new_parameters = (False, str(pd.Timestamp.now()), "Finished measurements")

    parameters.update(
        dict(zip(["measuring", "last_updated", "updated_action"], new_parameters))
    )

    with open(file, "w") as json_file:
        json.dump(parameters, json_file)

    return parameters


class Item(BaseModel):
    freq_sampling: float = 100
    time_measured: float = 2
    senoidal_amplitude: float = 1
    senoidal_frequency: float = 0.5
    last_updated: str = str(pd.Timestamp.now())
    updated_action: str = "Parameter modified - Test"


@app.post("/daq/parameters/modify")
def read_item(item: Item):
    file = "data_producer/signal/producer_parameters.json"
    new_parameter = item.dict()
    old_parameters = json.load(open(file))
    old_parameters.update(new_parameter)

    with open(file, "w") as json_file:
        json.dump(old_parameters, json_file)
    return old_parameters


@app.get("/dataset/data")
def get_dataset():

    data = manipulate_hdf5.read_all_data("measurements", "periodic_signal_group")

    return data.to_dict("records")
