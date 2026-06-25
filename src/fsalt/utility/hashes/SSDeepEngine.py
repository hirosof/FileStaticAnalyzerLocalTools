from rehashes import PySsdeep

from . import HashEngineBase


class SSDeepEngine(HashEngineBase.HashEngineBase):
    _internal_engine = None

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._internal_engine = PySsdeep()

    def update(self, data: bytes) -> None:
        self._internal_engine.update(data)

    def finalize(self) -> str:
        return self._internal_engine.finalize()

    @staticmethod
    def compute(data: bytes) -> str:
        engine = SSDeepEngine()
        engine.update(data)
        return engine.finalize()


if __name__ == "__main__":
    pass
