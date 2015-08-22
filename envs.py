import os
import yaml

def get_env(key):
    value = os.environ.get(key.upper())
    if value:
        return value
    else:
        environ_file = os.path.join(os.path.dirname(__file__), "./environ.yaml")
        with open(environ_file, "rb") as f:
            envs = yaml.load(f)
            value = envs[key.lower()]

    return value
