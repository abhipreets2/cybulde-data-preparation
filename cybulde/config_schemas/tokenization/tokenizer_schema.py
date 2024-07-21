from omegaconf import MISSING
from hydra.core.config_store import ConfigStore
from typing import Optional

from pydantic.dataclasses import dataclass

from cybulde.config_schemas.tokenization import pre_tokenizer_schema
from cybulde.config_schemas.tokenization import model_schema
@dataclass
class TokenizerConfig:
    _target_: str = MISSING

@dataclass
class HuggingFaceTokenizerConfig(TokenizerConfig):
    _target_: str = "cybulde.tokenization.tokenizers.HuggingFaceTokenizer"
    pre_tokenizer: pre_tokenizer_schema.PreTokenizerConfig = MISSING
    model: model_schema.ModelConfig = MISSING

    unk_token: Optional[str] = "[UNK]"
    cls_token: Optional[str] = "[CLS]"
    sep_token: Optional[str] = "[SEP]"
    pad_token: Optional[str] = "[PAD]"
    mask_token: Optional[str] = "[MASK]"


def setup_config() -> None:
    pre_tokenizer_schema.setup_config()
    model_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(
        group="tokenizer",
        name="hugging_face_tokenizer_schema",
        node=HuggingFaceTokenizerConfig,
    )
