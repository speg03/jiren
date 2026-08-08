import importlib.metadata

__version__ = importlib.metadata.version(__package__) if __package__ else "0+unknown"
