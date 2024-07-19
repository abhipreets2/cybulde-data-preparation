

from pydantic.dataclasses import dataclass

@dataclass
class TokenizerConfig:
    _target_: str = MISSING

@dataclass
class HuggingFaceTokenizerConfig(TokenizerConfig):
