import argparse
import json
from typing import Optional

from .client import client


def _response_to_json(dc: type) -> Optional[str]:
    output = {}

    try:
        for attr in dc.attrs():
            output[attr] = getattr(dc, attr)
    except AttributeError:
        pass

    return json.dumps(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="OBS websocket request command")
    parser.add_argument(
        "data",
        help="Options to pass to request, can be string or JSON",
        nargs="*",
        default=None,
    )

    args = parser.parse_args()

    handler_func = getattr(client, args.command)

    if handler_func is None:
        raise AttributeError(f"Invalid command: {args.command}")

    output: Optional[str] = None

    if len(args.data) == 0:
        output = handler_func()
    else:
        try:
            kwargs = json.loads(args.data[0])
            output = handler_func(**kwargs)
        except json.JSONDecodeError:
            output = handler_func(*args.data)

    print(_response_to_json(output))
