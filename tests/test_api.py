import httpx, json, pandas as pd


def test_alive():

    api_output = httpx.get("http://127.0.0.1:8000/alive")

    status = api_output.status_code

    assert 200 == status


def test_get_parameters():

    api_output = httpx.get("http://127.0.0.1:8000/daq/parameters")

    status = api_output.status_code

    content = json.loads(api_output.content)
    value = list(content.keys())

    expected = [
        "freq_sampling",
        "time_measured",
        "senoidal_amplitude",
        "senoidal_frequency",
        "noise_amplitude",
        "measuring",
        "last_updated",
        "updated_action",
    ]

    assert 200 == status and value == expected


def test_daq_start():

    api_output = httpx.get("http://127.0.0.1:8000/daq/start")

    status = api_output.status_code

    value = json.loads(api_output.content).get("measuring")

    expected = True

    assert 200 == status and value == expected


def test_daq_finish():

    api_output = httpx.get("http://127.0.0.1:8000/daq/finish")

    status = api_output.status_code

    value = json.loads(api_output.content).get("measuring")

    expected = False

    assert 200 == status and value == expected


def test_modify_parameters():

    new_parameters = {
        "freq_sampling": 100,
        "time_measured": 1.0,
        "senoidal_amplitude": 1.0,
        "senoidal_frequency": 10.0,
        "noise_amplitude": 1,
        "measuring": False,
        "last_updated": str(pd.Timestamp.now()),
        "updated_action": "New settings",
    }

    api_output = httpx.post(
        "http://127.0.0.1:8000/daq/parameters/modify",
        data=json.dumps(new_parameters),
    )

    status = api_output.status_code

    api_output_check = httpx.get("http://127.0.0.1:8000/daq/parameters")

    content = json.loads(api_output_check.content)
    breakpoint()
    assert 200 == status and new_parameters == content
