from abc import ABC, abstractmethod
from pathlib import Path

import core.vision_encoder.pe as pe
import core.vision_encoder.transforms as transforms
import torch
from PIL import Image


class DualEncoder(ABC):
    @abstractmethod
    def encode_vision(self, file: Path) -> torch.Tensor:
        ...
    
    @abstractmethod
    def encode_text(self, text: str) -> torch.Tensor:
        ...

    @abstractmethod
    def logit_scale(self) -> torch.Tensor:
        ...


class PerceptionEncoder(DualEncoder):
    def __init__(self, model_name: str = "PE-Core-L14-336") -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        self.model = pe.CLIP.from_config(model_name, pretrained=True)
        self.model = self.model.to(self.device)
        self.preprocess = transforms.get_image_transform(self.model.image_size)
        self.tokenizer = transforms.get_text_tokenizer(self.model.context_length)

    def encode_vision(self, file: Path) -> torch.Tensor:
        pil_image = Image.open(file)
        image = self.preprocess(pil_image).unsqueeze(0)
        image = image.to(self.device)
        with torch.inference_mode():
            image_features, _, _ = self.model(image, None)
        return image_features

    def encode_text(self, text: str) -> torch.Tensor:
        tokenized_text = self.tokenizer([text]).to(self.device)
        with torch.inference_mode():
            _, text_features, _ = self.model(None, tokenized_text)
        return text_features

    def logit_scale(self) -> torch.Tensor:
        return self.model.logit_scale.exp()
