import json
from pathlib import Path


def get_asset(name):
    path = Path(__file__).parent / "assets" / f"{name}.json"
    with open(path, "r") as f:
        return json.load(f)


def get_body_and_headers(asset_name):
    headers = get_asset(f"{asset_name}_request_headers")
    body = get_asset(f"{asset_name}_request_body")
    body["headers"] = headers

    return body, headers
