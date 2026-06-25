from fsalt.utility.hashes.CRC32Engine import CRC32Engine
from fsalt.utility.hashes.HashEngineBase import HashEngineBase
from fsalt.utility.hashes.MD5Engine import MD5Engine
from fsalt.utility.hashes.SHA1Engine import SHA1Engine
from fsalt.utility.hashes.SHA256Engine import SHA256Engine
from fsalt.utility.hashes.SSDeepEngine import SSDeepEngine
from fsalt.utility.hashes.TLSHEngine import TLSHEngine


class MultipleHashBulkEngine:
    engines: dict[str, dict[str, HashEngineBase]] = dict()

    def __init__(self):
        self.reset()
        return

    def reset(self):
        self.engines = {
            "Normal": {
                "CRC32": CRC32Engine(),
                "MD5": MD5Engine(),
                "SHA1": SHA1Engine(),
                "SHA256": SHA256Engine(),
            },
            "Fuzzy": {"ssdeep": SSDeepEngine(), "TLSH": TLSHEngine()},
        }
        return

    def update(self, data: bytes):
        for engine_dict in self.engines.values():
            for engine in engine_dict.values():
                engine.update(data)
        return

    def finalize(self) -> dict[str, dict[str, HashEngineBase]]:

        result_dict: dict[str, dict[str, HashEngineBase]] = dict()

        for engine_dict in self.engines.items():
            digest_dict: dict[str, str] = dict()
            for engine in engine_dict[1].items():
                digest_dict.update({engine[0]: engine[1].finalize()})
            result_dict.update({engine_dict[0]: digest_dict})

        return result_dict

    @staticmethod
    def compute(data: bytes) -> dict[str, dict[str, HashEngineBase]]:
        engine: MultipleHashBulkEngine = MultipleHashBulkEngine()
        engine.update(data)
        return engine.finalize()


if __name__ == "__main__":
    engine = MultipleHashBulkEngine()

    engine.update(
        # b"Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod"
        b"abcdef"
    )
    import json

    print(json.dumps(engine.finalize(), indent=2))
