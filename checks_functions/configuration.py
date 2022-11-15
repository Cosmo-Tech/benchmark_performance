""".env"""
from cosmotech_api import Configuration

def get_configuration(host: str, token: str):
    """.env"""
    configuration = Configuration(
            host=host,
            discard_unknown_keys=True,
            access_token=token)
    return configuration
    