from omegaconf import MISSING
from hydra.core.config_store import ConfigStore
from typing import Optional

from pydantic.dataclasses import dataclass

from cybulde.config_schemas.tokenization import pre_tokenizer_schema
from cybulde.config_schemas.tokenization import model_schema
from cybulde.config_schemas.tokenization import trainer_schema
from cybulde.config_schemas.tokenization import normalizer_schema
from cybulde.config_schemas.tokenization import decoder_schema
from cybulde.config_schemas.tokenization import post_processor_schema

@dataclass
class TokenizerConfig:
    _target_: str = MISSING

@dataclass
class HuggingFaceTokenizerConfig(TokenizerConfig):
    _target_: str = "cybulde.tokenization.tokenizers.HuggingFaceTokenizer"
    pre_tokenizer: pre_tokenizer_schema.PreTokenizerConfig = MISSING
    model: model_schema.ModelConfig = MISSING
    trainer: trainer_schema.TrainerConfig = MISSING
    normalizer: Optional[normalizer_schema.NormalizerConfig] = None
    decoder: Optional[decoder_schema.DecoderConfig] = None
    post_processor: Optional[post_processor_schema.PostProcessorConfig] = None
    
    unk_token: Optional[str] = "[UNK]"
    cls_token: Optional[str] = "[CLS]"
    sep_token: Optional[str] = "[SEP]"
    pad_token: Optional[str] = "[PAD]"
    mask_token: Optional[str] = "[MASK]"


def setup_config() -> None:
    pre_tokenizer_schema.setup_config()
    model_schema.setup_config()
    trainer_schema.setup_config()
    normalizer_schema.setup_config()
    decoder_schema.setup_config()
    post_processor_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(
        group="tokenizer",
        name="hugging_face_tokenizer_schema",
        node=HuggingFaceTokenizerConfig,
    )
