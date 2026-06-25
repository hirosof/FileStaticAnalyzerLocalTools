import tlsh

from . import HashEngineBase


class TLSHEngine(HashEngineBase.HashEngineBase):
    _internal_engine = None
    _finalized = False
    _length = 0

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._internal_engine = tlsh.Tlsh()
        _finalized = False
        _length = 0

    def update(self, data: bytes) -> None:
        self._internal_engine.update(data)
        self._length += len(data)

    def finalize(self) -> str:

        if self._length < 50:
            return "TLESS"

        if self._finalized is False:
            self._internal_engine.final()
            self._finalized = True

        if self._internal_engine.is_valid:
            return self._internal_engine.hexdigest()

        return "TNULL"

    @staticmethod
    def compute(data: bytes) -> str:
        engine = TLSHEngine()
        engine.update(data)
        return engine.finalize()


if __name__ == "__main__":
    pass
