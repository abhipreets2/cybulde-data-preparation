from cybulde.utils.gcp_utils import access_secret_version
import dask.dataframe as dd
from typing import Optional
from shutil import rmtree
from cybulde.utils.utils import run_shell_command
import psutil
import pkg_resources
import symspellpy
from symspellpy import SymSpell
import pandas as pd

def filter_based_on_minimum_number_of_words(df: pd.DataFrame, min_nrof_words: int) -> pd.DataFrame:
    return df[df["cleaned_text"].str.split().apply(len) >= min_nrof_words]


def get_cmd_to_get_raw_data(
    version: str,
    data_local_save_dir: str,
    dvc_remote_repo: str,
    dvc_data_folder: str,
    github_user_name: str,
    github_access_token: str,
    ) -> str:
    without_https = dvc_remote_repo.replace("https://", "")
    dvc_remote_repo = f"https://{github_user_name}:{github_access_token}@{without_https}"
    command = f"dvc get {dvc_remote_repo} {dvc_data_folder} --rev {version} -o {data_local_save_dir}"
    return command

def get_raw_data_with_version(
    version: str,
    data_local_save_dir: str,
    dvc_remote_repo: str,
    dvc_data_folder: str,
    github_user_name: str,
    github_access_token: str,
) -> None:
    rmtree(data_local_save_dir, ignore_errors=True)
    command = get_cmd_to_get_raw_data(
        version, data_local_save_dir, dvc_remote_repo, dvc_data_folder, github_user_name, github_access_token
    )
    run_shell_command(command)


def repartition_dataframe(
        df: dd.core.DataFrame,
        nrof_workers: int,
        available_memory: Optional[float] = None,
        min_partition_size: int = 15 * 1024**2,
        aimed_nrof_partitions_per_worker: int = 10,
        ) -> dd.core.DataFrame:
        df_memory_usage = df.memory_usage(deep=True).sum().compute()
        nrof_partitions = get_nrof_partitions(
        df_memory_usage, nrof_workers, available_memory, min_partition_size, aimed_nrof_partitions_per_worker
    )
        partitioned_df: dd.core.DataFrame = df.repartition(npartitions=1).repartition(npartitions=nrof_partitions)  
        return partitioned_df

def get_repo_address_with_access_token(
        gcp_project_id: str,
        gcp_github_access_token_secret_id: str,
        dvc_remote_repo: str,
        github_user_name: str
        ) -> str:
    access_token = access_secret_version(gcp_project_id, gcp_github_access_token_secret_id)
    repo_address = dvc_remote_repo.replace("https://", "")
    return f"https://{github_user_name}:{access_token}@{repo_address}"

def get_nrof_partitions(
    df_memory_usage: int,
    nrof_workers: int,
    available_memory: Optional[float],
    min_partition_size: int,
    aimed_nrof_partitions_per_worker: int,
) -> int:
    if available_memory is None:
        available_memory = psutil.virtual_memory().available
    else:
        available_memory = available_memory * nrof_workers

    if df_memory_usage <= min_partition_size:
        return 1

    if df_memory_usage / nrof_workers <= min_partition_size:
        return round(df_memory_usage / min_partition_size)

    nrof_partitions_per_worker = 0
    required_memory = float("inf")

    while required_memory > available_memory:
        nrof_partitions_per_worker += 1
        required_memory = df_memory_usage / nrof_partitions_per_worker

    nrof_partitions = nrof_partitions_per_worker * nrof_workers

    while (df_memory_usage / (nrof_partitions + 1)) > min_partition_size and (
        nrof_partitions // nrof_workers
    ) < aimed_nrof_partitions_per_worker:
        nrof_partitions += 1

    return nrof_partitions


class SpellCorrectionModel:
    def __init__(
        self,
        max_dictionary_edit_distance: int = 2,
        prefix_length: int = 7,
        count_threshold: int = 1,
    ) -> None:
        self.max_dictionary_edit_distance = max_dictionary_edit_distance
        self.model = self._initialize_model(prefix_length, count_threshold)

    def _initialize_model(self, prefix_length: int, count_threshold: int) -> symspellpy.symspellpy.SymSpell:
        model = SymSpell(self.max_dictionary_edit_distance, prefix_length, count_threshold)

        dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
        bigram_dictionary_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt"
        )

        model.load_dictionary(dictionary_path, 0, 1)
        model.load_bigram_dictionary(bigram_dictionary_path, 0, 2)
        return model
