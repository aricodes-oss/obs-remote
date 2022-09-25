import obsws_python as obs
import toml
import os

config_path = os.path.expanduser("~/.obs-remote.toml")

if not os.path.exists(config_path):
    raise OSError("~/.obs-remote.toml does not exist")

with open(config_path) as f:
    config_data = toml.load(f)

client = obs.ReqClient(**config_data)
