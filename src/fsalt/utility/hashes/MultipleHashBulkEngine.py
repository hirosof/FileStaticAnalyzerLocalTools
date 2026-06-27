import json
from enum import Enum
from pathlib import Path
from typing import Annotated

import rich.progress
import typer

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

    def finalize(self) -> dict[str, dict[str, str]]:

        result_dict: dict[str, dict[str, str]] = dict()

        for engine_dict in self.engines.items():
            digest_dict: dict[str, str] = dict()
            for engine in engine_dict[1].items():
                digest_dict.update({engine[0]: engine[1].finalize()})
            result_dict.update({engine_dict[0]: digest_dict})

        return result_dict

    @staticmethod
    def compute(data: bytes) -> dict[str, dict[str, str]]:
        engine: MultipleHashBulkEngine = MultipleHashBulkEngine()
        engine.update(data)
        return engine.finalize()


#
#  以下 CLIインタフェース用の実装
#


app = typer.Typer(no_args_is_help=True)


class ResultFormat(str, Enum):
    Json = "Json"
    Markdown = "Markdown"


def print_result(result: dict, type: ResultFormat):
    match type:
        case ResultFormat.Json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        case ResultFormat.Markdown:
            for current in result.items():
                print(f"## {current[0]}\n")

                for type_item in current[1].items():
                    print(f"### {type_item[0]}\n")

                    print("|Name|Value|")
                    print("|---|---|")

                    for item in type_item[1].items():
                        print(f"|`{item[0]}`|`{item[1]}`|")

                    print()


@app.command("string")
def process_string(
    target: Annotated[str, typer.Argument(help="算出対象文字列")],
    charset: Annotated[str, typer.Option(help="文字コード名")] = "utf-8",
    format: Annotated[
        ResultFormat, typer.Option(help="出力フォーマット")
    ] = ResultFormat.Markdown,
):

    enc_data = target.encode(encoding=charset)

    result = MultipleHashBulkEngine.compute(enc_data)

    print_result({target: result}, format)


def get_file_hashes(target: Path) -> dict | None:

    if target.is_file() is False:
        return None

    file_size = target.stat().st_size

    progress = rich.progress.Progress(
        rich.progress.TextColumn("[bold blue]{task.description}"),
        rich.progress.BarColumn(),  # バー本体
        rich.progress.TaskProgressColumn(),  # パーセント表示 (例: 50%)
        rich.progress.TimeRemainingColumn(),  # 残り時間の予測 (例: 0:03))
        transient=True,
    )

    load_task = progress.add_task("読み込み中")
    task = progress.add_task("計算中", total=file_size)

    engine = MultipleHashBulkEngine()
    progress.start()
    with progress.open(file=target, mode="rb", task_id=load_task) as file:
        while data := file.read(1024 * 1024 * 32):
            engine.update(data)
            progress.update(task, advance=len(data))

    result = engine.finalize()

    progress.stop()
    return result


@app.command("file")
def process_file(target: Annotated[Path, typer.Argument(help="算出対象ファイルパス")]):

    print_result({str(target): get_file_hashes(target)}, ResultFormat.Json)


@app.command("folder")
def process_folder(
    target: Annotated[Path, typer.Argument(help="算出対象フォルダパス")],
):
    pass


if __name__ == "__main__":
    app()
