import os
from pathlib import Path
from hydra.utils import instantiate
import hydra
from cybulde.utils.utils import get_logger
from cybulde.utils.config_utils import get_config
from omegaconf import OmegaConf
import pandas as pd

@get_config(config_path="../configs", config_name="tokenizer_training_config")
def train_tokenizer(config) -> None:
    os.environ["HYDRA_FULL_ERROR"] = "1"
    logger = get_logger(Path(__file__).name)
    print(OmegaConf.to_yaml(config, resolve=True))
    data_parquet_path = config.data_parquet_path
    text_column_name = config.text_column_name
    trained_tokenizer_path = config.trained_tokenizer_path

    tokenizer = instantiate(config.tokenizer, _convert_="all")

    logger.info("Reading dataset...")
    df = pd.read_parquet(data_parquet_path)

    logger.info("Starting training...")
    tokenizer.train(df[text_column_name].values)

    logger.info("Saving tokenizer...")

    tokenizer_save_dir = os.path.join(trained_tokenizer_path, "trained_tokenizer")
    tokenizer.save(tokenizer_save_dir)

    logger.info("Saved tokenizer.")


if __name__=="__main__":
    train_tokenizer()
