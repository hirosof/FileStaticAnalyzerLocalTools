import hashlib

from . import HashEngineBase


class SHA256Engine(HashEngineBase.HashEngineBase):
    _internal_engine = None

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._internal_engine = hashlib.sha256()

    def update(self, data: bytes) -> None:
        self._internal_engine.update(data)

    def finalize(self) -> str:
        return self._internal_engine.hexdigest()

    @staticmethod
    def compute(data: bytes) -> str:
        engine = SHA256Engine()
        engine.update(data)
        return engine.finalize()


if __name__ == "__main__":
    pass
