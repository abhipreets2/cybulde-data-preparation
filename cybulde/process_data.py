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

def process_raw_data(
        df_partition: dd.core.DataFrame,
        dataset_cleaner_manager: DatasetCleanerManager
        ) -> dd.core.Series:
    return df_partition["text"].apply(dataset_cleaner_manager)


@get_config(config_path="../configs", config_name="config")
def process_data(config) -> None:
    os.environ["HYDRA_FULL_ERROR"] = "1"
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")
    print(OmegaConf.to_yaml(config, resolve=True))
    processed_data_save_dir = config.processed_data_save_dir
    if (config.fetch_data):
        logger.info("Fetching data...")
        get_raw_data_with_version(version=config.version, data_local_save_dir=config.data_local_save_dir, dvc_remote_repo=config.dvc_remote_repo, dvc_data_folder=config.dvc_data_folder, github_user_name=config.github_user_name, github_access_token=access_secret_version(config.infrastructure.project_id, config.github_access_token_secret_id))
        logger.info("Data stored in local.")
    cluster =custom_instantiate(config.dask_cluster) 
    client = Client(cluster)

    try:
        logger.info("Reading dataset...")
        dataset_reader_manager = instantiate(config.dataset_reader_manager)
        df = dataset_reader_manager.read_data(nrof_workers=config.dask_cluster.n_workers)
        logger.info(f"Number of partitions for dataframe: {df.npartitions}")
        logger.info("Cleaning dataset...")
        dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)
        # using map_partitions to process each partition parallelly
        df = df.assign(
                cleaned_text=df.map_partitions(
                    process_raw_data, dataset_cleaner_manager=dataset_cleaner_manager, meta=("text", "object")))
        df = df.compute()

        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
        test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")

        train_df = df[df["split"] == "train"]
        dev_df = df[df["split"] == "dev"]
        test_df = df[df["split"] == "test"]

        train_df = filter_based_on_minimum_number_of_words(train_df, min_nrof_words=config.min_nrof_words)
        dev_df = filter_based_on_minimum_number_of_words(dev_df, min_nrof_words=config.min_nrof_words)
        test_df = filter_based_on_minimum_number_of_words(test_df, min_nrof_words=config.min_nrof_words)

        train_df.to_parquet(train_parquet_path)
        dev_df.to_parquet(dev_parquet_path)
        test_df.to_parquet(test_parquet_path)

        logger.info("Data processing finished!")
    
    finally:
        logger.info("closing dask client and cluster...")
        client.close()
        cluster.close()

if __name__=="__main__":
    process_data()
