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
from cybulde.utils.data_utils import get_raw_data_with_version, filter_based_on_minimum_number_of_words
from cybulde.utils.gcp_utils import access_secret_version
import dask.dataframe as dd
from cybulde.data_processing.dataset_cleaner import DatasetCleanerManager
from cybulde.utils.config_utils import custom_instantiate

@get_config(config_path="../configs", config_name="tokenizer_training_config")
def train_tokenizer(config) -> None:
    os.environ["HYDRA_FULL_ERROR"] = "1"
    logger = get_logger(Path(__file__).name)
    print(OmegaConf.to_yaml(config, resolve=True))
    exit(0)

if __name__=="__main__":
    train_tokenizer()
