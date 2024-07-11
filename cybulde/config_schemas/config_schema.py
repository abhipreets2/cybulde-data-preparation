from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass
from omegaconf import MISSING
from cybulde.config_schemas.dask_cluster import dask_cluster_schema
from cybulde.config_schemas.data_processing import dataset_readers_schema, dataset_cleaner_schema
from cybulde.config_schemas.infrastructure import gcp_schema

@dataclass 
class Config:
    version: str = MISSING
    fetch_data: bool = MISSING
    data_local_save_dir: str = "./data/raw"
    dvc_remote_repo: str = "https://github.com/abhipreets2/cybulde-data-versioning.git"
    dvc_data_folder: str = "data/raw"
    github_user_name: str = "abhipreets2"
    github_access_token_secret_id: str = "github-access-token"
    infrastructure: gcp_schema.GCPConfig = gcp_schema.GCPConfig()
    dask_cluster: dask_cluster_schema.DaskClusterConfig = MISSING
    dataset_reader_manager: dataset_readers_schema.DatasetReaderManagerConfig = MISSING
    dataset_cleaner_manager: dataset_cleaner_schema.DatasetCleanerManagerConfig = MISSING

def setup_config():
    dask_cluster_schema.setup_config()
    dataset_readers_schema.setup_config()
    dataset_cleaner_schema.setup_config()
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
