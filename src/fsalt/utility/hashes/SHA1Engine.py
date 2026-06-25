import hashlib

from . import HashEngineBase


class SHA1Engine(HashEngineBase.HashEngineBase):
    _internal_engine = None

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._internal_engine = hashlib.sha1()

    def update(self, data: bytes) -> None:
        self._internal_engine.update(data)

    def finalize(self) -> str:
        return self._internal_engine.hexdigest()

    @staticmethod
    def compute(data: bytes) -> str:
        engine = SHA1Engine()
        engine.update(data)
        return engine.finalize()


if __name__ == "__main__":
    pass
