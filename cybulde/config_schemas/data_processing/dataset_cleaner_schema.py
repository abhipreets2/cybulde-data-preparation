from pydantic.dataclasses import dataclass
from omegaconf import MISSING
import string
from dataclasses import field
from hydra.core.config_store import ConfigStore

@dataclass
class SpellCorrectionModelConfig:
    _target_: str = "cybulde.utils.utils.SpellCorrectionModel"
    max_dictionary_edit_distance: int = 2
    prefix_length: int = 7
    count_threshold: int = 1

@dataclass
class DatasetCleanerConfig:
    _target_: str = MISSING


@dataclass
class StopWordsDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.StopWordsDatasetCleaner"


@dataclass
class ToLowerCaseDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.ToLowerCaseDatasetCleaner"


@dataclass
class URLDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.URLDatasetCleaner"


@dataclass
class PunctuationDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.PunctuationDatasetCleaner"
    punctuation: str = string.punctuation


@dataclass
class NonLettersDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.NonLettersDatasetCleaner"


@dataclass
class NewLineCharacterDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.NewLineCharacterDatasetCleaner"


@dataclass
class NonASCIIDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.NonASCIIDatasetCleaner"


@dataclass
class ReferenceToAccountDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.ReferenceToAccountDatasetCleaner"


@dataclass
class ReTweetDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.ReTweetDatasetCleaner"


@dataclass
class SpellCorrectionDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.SpellCorrectionDatasetCleaner"
    spell_correction_model: SpellCorrectionModelConfig = SpellCorrectionModelConfig()


@dataclass
class CharacterLimiterDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "cybulde.data_processing.dataset_cleaner.CharacterLimiterDatasetCleaner"
    character_limit: int = 300


@dataclass
class DatasetCleanerManagerConfig:
    _target_: str = "cybulde.data_processing.dataset_cleaner.DatasetCleanerManager"
    # defaulted to empty dictionary if, we want to used raw data
    dataset_cleaners: dict[str, DatasetCleanerConfig] = field(default_factory=lambda: {})


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="stop_words_dataset_cleaner_schema",
        node=StopWordsDatasetCleanerConfig,
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="to_lower_case_dataset_cleaner_schema",
        node=ToLowerCaseDatasetCleanerConfig,
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner", name="url_dataset_cleaner_schema", node=URLDatasetCleanerConfig
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="punctuation_dataset_cleaner_schema",
        node=PunctuationDatasetCleanerConfig,
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="non_letters_dataset_cleaner_schema",
        node=NonLettersDatasetCleanerConfig,
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="new_line_character_dataset_cleaner_schema",
        node=NewLineCharacterDatasetCleanerConfig,
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="non_ascii_dataset_cleaner_schema",
        node=NonASCIIDatasetCleanerConfig,
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="reference_to_account_dataset_cleaner_schema",
        node=ReferenceToAccountDatasetCleanerConfig,
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="re_tweet_dataset_cleaner_schema",
        node=ReTweetDatasetCleanerConfig,
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="spell_correction_dataset_cleaner_schema",
        node=SpellCorrectionDatasetCleanerConfig,
    )

    cs.store(
        group="dataset_cleaner_manager/dataset_cleaner",
        name="character_limiter_dataset_cleaner_schema",
        node=CharacterLimiterDatasetCleanerConfig,
    )

    cs.store(group="dataset_cleaner_manager", name="dataset_cleaner_manager_schema", node=DatasetCleanerManagerConfig)

