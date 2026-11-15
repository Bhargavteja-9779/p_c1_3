"""Allow-listed unpickler for the HUST dataset.

The HUST release (Ma et al., Energy Environ. Sci. 2022; Mendeley Data nsc7hnsg4s)
is distributed as Python pickles of pandas DataFrames. Unpickling untrusted data can
execute arbitrary code, so only numpy/pandas reconstruction helpers and
``builtins.slice`` are permitted; anything else raises ``pickle.UnpicklingError``.
"""
import io
import pickle

_ALLOWED_PREFIXES = ("numpy", "pandas")
_ALLOWED_BUILTINS = {"slice"}


class _RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "builtins" and name in _ALLOWED_BUILTINS:
            return super().find_class(module, name)
        if module.split(".")[0] in _ALLOWED_PREFIXES:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"blocked global {module}.{name}")


def safe_load(path):
    with open(path, "rb") as f:
        return _RestrictedUnpickler(io.BytesIO(f.read())).load()
