from typing import Optional
from cybulde.utils.data_utils import get_repo_address_with_access_token
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, SI
from pydantic.dataclasses import dataclass

@dataclass
class DatasetReaderConfig:
    _target_: str = MISSING
    dataset_dir: str = MISSING
    dataset_name: str = MISSING
    gcp_project_id: str = SI("${infrastructure.project_id}")
    gcp_github_access_token_secret_id: str = SI("${github_access_token_secret_id}")
    dvc_remote_repo: str = SI("${dvc_remote_repo}")
    github_user_name: str = SI("${github_user_name}")
    version: str = SI("${version}")

@dataclass
class GHCReaderConfig(DatasetReaderConfig):
    _target_: str = "cybulde.data_processing.dataset_readers.GHCDatasetReader"
    dev_split_ratio: float = MISSING

@dataclass
class JigsawReaderConfig(DatasetReaderConfig):
    _target_: str = "cybulde.data_processing.dataset_readers.JigsawDatasetReader"
    dev_split_ratio: float = MISSING

@dataclass
class TwitterReaderConfig(DatasetReaderConfig):
    _target_: str = "cybulde.data_processing.dataset_readers.TwitterDatasetReader"
    dev_split_ratio: float = MISSING
    test_split_ratio: float = MISSING


@dataclass
class DatasetReaderManagerConfig:
    _target_: str = "cybulde.data_processing.dataset_readers.DatasetReaderManager" 
    dataset_readers: dict[str, DatasetReaderConfig] = MISSING
    repartition: bool = True
    available_memory: Optional[float] = None

def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="dataset_reader_manager_schema", node=DatasetReaderManagerConfig, group="dataset_reader_manager")
    cs.store(name="ghc_dataset_reader_schema", node=GHCReaderConfig, group="dataset_reader_manager/dataset_reader")
    cs.store(name="jigsaw_dataset_reader_schema", node=JigsawReaderConfig, group="dataset_reader_manager/dataset_reader")
    cs.store(name="twitter_dataset_reader_schema", node=TwitterReaderConfig, group="dataset_reader_manager/dataset_reader")
