from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass
from omegaconf import MISSING
from cybulde.config_schemas.dask_cluster import dask_cluster_schema
from cybulde.config_schemas.data_processing import dataset_readers_schema

@dataclass 
class Config:
    dask_cluster: dask_cluster_schema.DaskClusterConfig = MISSING
    dataset_reader_manager: dataset_readers_schema.DatasetReaderConfig = MISSING

def setup_config():
    dask_cluster_schema.setup_config()
    dataset_readers_schema.setup_config()
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
