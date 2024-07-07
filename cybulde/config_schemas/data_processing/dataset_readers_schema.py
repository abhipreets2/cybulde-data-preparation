from typing import Optional
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

def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="dataset_reader_manager_schema", node=DatasetReaderConfig, group="dataset_reader_manager")
