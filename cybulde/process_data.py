import os
from pathlib import Path
import dask.dataframe as dd
from dask.distributed import Client
from dask.distributed import LocalCluster
from hydra.utils import instantiate
import hydra
from cybulde.config_schemas.dask_cluster.dask_cluster_schema import setup_config
from cybulde.utils.utils import get_logger
from cybulde.utils.config_utils import get_config

@get_config(config_path="../configs", config_name="config")
def process_data(config) -> None:
    os.environ["HYDRA_FULL_ERROR"] = "1"
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")
    print(config)
    cluster = instantiate(config.dask_cluster) 
    client = Client(cluster)
    print(client)
if __name__=="__main__":
    process_data()
