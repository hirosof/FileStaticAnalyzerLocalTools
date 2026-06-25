class HashEngineBase:
    def __init__(self):
        pass

    def reset(self) -> None:
        pass

    def update(self, data: bytes) -> None:
        pass

    def finalize(self) -> str:
        pass

    @staticmethod
    def compute(data: bytes) -> str:
        pass
