from telnetlib import OUTMRK
import h5py
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def create_long_term_file(filename: str, group: str):

    hierarchicalFileName = f"data_storage/{filename}.hdf5"

    hierarchicalFile = h5py.File(hierarchicalFileName, "w")

    hierarchicalFile.create_group(group)


def dataset_insert(filename: str, group: str, dataset: str, message: dict):

    f = h5py.File(f"data_storage/{filename}.hdf5", "a")

    f.create_dataset(f"/{group}/{dataset}", data=np.array(message))

    f.close()

    print("Dataset saved")


def dataset_del(filename: str, group: str, dataset: str):

    with h5py.File(f"data_storage/{filename}.hdf5", "a") as f:

        del f[f"/{group}/{dataset}"]

    print("Dataset deleted")


def read_all_data(filename: str, group: str):

    f = h5py.File(f"data_storage/{filename}.hdf5", "r")

    data = f.get(group)
    all_data = pd.DataFrame()

    for dataset in data.keys():
        all_data = all_data.append(
            {
                "id": dataset,
                "time": np.array(data[dataset])[0].tolist(),
                "signal": np.array(data[dataset])[1].tolist(),
            },
            ignore_index=True,
        )

    return all_data
