from cybulde.utils.gcp_utils import access_secret_version
import dask.dataframe as dd
from typing import Optional
from shutil import rmtree
from cybulde.utils.utils import run_shell_command

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
