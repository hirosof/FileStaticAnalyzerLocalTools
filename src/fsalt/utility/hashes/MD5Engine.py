import hashlib

from fsalt.utility.hashes.HashEngineBase import HashEngineBase


class MD5Engine(HashEngineBase):
    _internal_engine = None

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._internal_engine = hashlib.md5()

    def update(self, data: bytes) -> None:
        self._internal_engine.update(data)

    def finalize(self) -> str:
        return self._internal_engine.hexdigest()

    @staticmethod
    def compute(data: bytes) -> str:
        engine = MD5Engine()
        engine.update(data)
        return engine.finalize()


if __name__ == "__main__":
    pass
