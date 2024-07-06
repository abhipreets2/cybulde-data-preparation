import os
from pathlib import Path
import dask.dataframe as dd
from dask.distributed import Client
from dask.distributed import LocalCluster
from hydra.utils import instantiate
import hydra
from cybulde.config_schemas.dask_cluster.dask_cluster_schema import setup_config
from cybulde.utils.utils import get_logger

setup_config()
@hydra.main(config_path="./configs", config_name="config", version_base=None)
def process_data(config) -> None:
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")
    print(config)
#    processed_data_save_dir = config.processed_data_save_dir
#    cluster = instantiate(config) 
#    client = Client(cluster)
#    print(client)
if __name__=="__main__":
    process_data()
