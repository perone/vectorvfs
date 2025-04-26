from dataclasses import dataclass, field
from pathlib import Path

import click
import torch
from rich.console import Console

from vectorvfs.utils import PerfCounter
from vectorvfs.vfsstore import VFSStore, XAttrFile

console = Console()


@dataclass(order=True)
class PathSimilarity:
    path: Path = field(compare=False)
    similarity: float


@click.group()
def vfs():
    """VectorVFS command line interface."""
    pass


@vfs.command()
@click.option(
    '-n', '--num', 'n', required=True, type=int, default=5,
    help='Number of results to return'
)
@click.argument('query', type=str)
@click.argument(
    'path',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    metavar='PATH')
@click.option('--force-reindex', '-f', is_flag=True, default=False, help="Forces reindexing.")
def search(n: int, query: str, path: str, force_reindex: bool) -> None:
    """Search files by similarity."""
    with console.status("", speed=1, spinner="bouncingBall") as status:
        status.update("Loading Perception Encoder model...")

        with PerfCounter() as model_counter:
            from vectorvfs.encoders import PerceptionEncoder
            pe_encoder = PerceptionEncoder("PE-Core-B16-224")
            logit_scale = pe_encoder.logit_scale()

        console.log(f"Perception Encoder model [bold cyan]{pe_encoder.model_name}[/bold cyan] "
                    f"loaded in [bold cyan]{model_counter.elapsed:.2f}s[/bold cyan].")

        status.update("Encoding search query...")
        with PerfCounter() as query_counter:
            query_features = pe_encoder.encode_text(query).to(torch.float16)

        console.log(f"Query encoded in [bold cyan]{query_counter.elapsed:.2f}s[/bold cyan].")
        status.update("Processing files...")

        feature_stack = []
        file_stack = []
        for pathfile in Path(path).iterdir():
            if not pathfile.is_file():
                continue

            if pathfile.suffix != ".jpg":
                continue

            console.log(f"Processing [bold blue]{pathfile}[/bold blue]")
            xattrfile = XAttrFile(pathfile)
            vfs_store = VFSStore(xattrfile)
            keys = xattrfile.list()
            if "user.vectorvfs" not in keys or force_reindex:
                console.log("[bold blue]{pathfile}[/bold blue] not indexed, indexing...")
                features = pe_encoder.encode_vision(pathfile)
                features = features.to(torch.float16)
                vfs_store.write_tensor(features)
            else:
                features = vfs_store.read_tensor()
            feature_stack.append(features)
            file_stack.append(pathfile)
        
        feature_stack = torch.vstack(feature_stack)

        with torch.inference_mode():
            text_probs = feature_stack @ query_features.T
        
        text_probs = text_probs.flatten()
        text_argsort = text_probs.argsort(descending=True)
        console.log(f"\nTop {n} files found:")
        for idx in text_argsort[:n]:
            console.log(f"[bold blue]{file_stack[idx].name}[/bold blue] "
                        f"(Similarity -> {text_probs[idx]:.3f})")


if __name__ == '__main__':
    vfs()
