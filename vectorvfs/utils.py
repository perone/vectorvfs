import time
from PIL import Image
from contextlib import ContextDecorator
from pathlib import Path
from typing import Callable, Dict, Set
import torch

class PerfCounter(ContextDecorator):
    """
    Context manager and decorator to measure elapsed time.

    Usage as a context manager:
        with PerfCounter():
            ...  # code to time

    Usage as a decorator:
        @PerfCounter()
        def foo(...):
            ...

    The elapsed time is printed on exit.
    """
    def __init__(self) -> None:
        self.start = None
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end = time.perf_counter()
        self.elapsed = end - self.start


def pillow_image_extensions():
    Image.init()
    return {
        ext.lower()
        for ext, fmt in Image.registered_extensions().items()
        if (
            fmt in Image.OPEN
            and Image.MIME.get(fmt, "").startswith("image/")
        )
    }


def extract_pdf_text(pdf_path: Path) -> str:
    """
    Extract text from a PDF file using PyPDF2.
    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def supported_files() -> Set[str]:
    """
    Returns a set of all supported file extensions.
    """
    return pillow_image_extensions() | {'.pdf'}


def extract_image_features(image_path: Path, encoder) -> torch.Tensor:
    """
    Extract features from an image file.
    """
    features = encoder.encode_vision(image_path)
    return features


def extract_pdf_features(pdf_path: Path, encoder) -> torch.Tensor:
    """
    Extract features from a PDF file by encoding its text content.
    """
    text = extract_pdf_text(pdf_path)
    features = encoder.encode_text(text)
    return features


def get_feature_extractor(extension: str) -> Callable[[Path, object], torch.Tensor]:
    """
    Returns the appropriate feature extraction function for a given file extension.
    """
    extractors: Dict[str, Callable[[Path, object], torch.Tensor]] = {
        '.pdf': extract_pdf_features,
    }
    
    # Add all image extensions to use the image extractor
    for ext in pillow_image_extensions():
        extractors[ext] = extract_image_features
        
    return extractors.get(extension.lower())
