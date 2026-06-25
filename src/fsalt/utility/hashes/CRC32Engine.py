import fastcrc

from . import HashEngineBase


class CRC32Engine(HashEngineBase.HashEngineBase):
    _value = 0

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._value = fastcrc.crc32.iso_hdlc(b"")

    def update(self, data: bytes) -> None:
        self._value = fastcrc.crc32.iso_hdlc(data, initial=self._value)
        return

    def finalize(self) -> str:
        return f"{self._value:08x}"

    @staticmethod
    def compute(data: bytes) -> str:
        engine = CRC32Engine()
        engine.update(data)
        return engine.finalize()


if __name__ == "__main__":
    pass
