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
from omegaconf import OmegaConf
from cybulde.utils.data_utils import get_raw_data_with_version
from cybulde.utils.gcp_utils import access_secret_version

@get_config(config_path="../configs", config_name="config")
def process_data(config) -> None:
    os.environ["HYDRA_FULL_ERROR"] = "1"
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")
    print(OmegaConf.to_yaml(config))
    if (config.fetch_data):
        logger.info("Fetching data...")
        get_raw_data_with_version(version=config.version, data_local_save_dir=config.data_local_save_dir, dvc_remote_repo=config.dvc_remote_repo, dvc_data_folder=config.dvc_data_folder, github_user_name=config.github_user_name, github_access_token=access_secret_version(config.infrastructure.project_id, config.github_access_token_secret_id))
        logger.info("Data stored in local.")
    exit(0)
    cluster = instantiate(config.dask_cluster) 
    client = Client(cluster)

    try:
        logger.info("reading dataset...")
        dataset_reader_manager = instantiate(config.dataset_reader_manager)
        print(dataset_reader_manager)
    finally:
        logger.info("closing dask client and cluster...")
        client.close()
        cluster.close()

if __name__=="__main__":
    process_data()
