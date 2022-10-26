import pathlib
import json
from uuid import uuid4


def get_token():
    p = pathlib.Path.home() / ".loopbackd"
    if p.exists():
        with p.open("r") as loopbackd_conf:
            return json.load(loopbackd_conf)["token"]
    else:
        with p.open("w") as loopbackd_conf:
            token = f"loopback:{uuid4().hex}"
            json.dump({"token": token}, loopbackd_conf)
            return token
