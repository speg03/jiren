try:
    import importlib.metadata as metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore

jiren_version = metadata.version("jiren")
jinja2_version = metadata.version("jinja2")
