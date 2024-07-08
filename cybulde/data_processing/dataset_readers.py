from abc import  ABC, abstractmethod
from cybulde.utils.utils import get_logger
from cybulde.utils.data_utils import get_repo_address_with_access_token
import dask.dataframe as dd
from typing import Optional
import os

class DatasetReader(ABC):
    required_columns = {"text", "label", "split", "dataset_name"}
    split_names = {"train", "dev", "test"}

    def __init__(
            self,
            dataset_dir: str,
            dataset_name: str,
            gcp_project_id: str,
            gcp_github_access_token_scret_id: str,
            dvc_remote_repo: str,
            github_user_name: str,
            version: str
            ) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.dataset_dir = dataset_dir
        self.dataset_name = dataset_name
        self.dvc_remote_repo = get_repo_address_with_access_token(
            gcp_project_id, gcp_github_access_token_secret_id, dvc_remote_repo, github_user_name
        ) 
        self.version = version

    def read_data(self) -> dd.core.DataFrame:
        self.logger.info(f"Reading {self.__class__.__name__}")
        train_df, dev_df, test_df = self._read_data()
        df = self.assign_split_names_to_data_frames_and_merge(train_df, dev_df, test_df)
        df["dataset_name"] = self.dataset_name
        if any(required_column not in df.columns.values for required_column in self.required_coulmns):
            raise ValueError(f"Dataset must contain all required columns: {self.required_columns}")
        unique_split_names = set(df["split"].unique().compute().tolist())
        if unique_split_names != self.split_names:
            raise ValueError(f"Dataset must contain all required split names: {self.split_names}")

        final_df = df[list(self.required_columns)]
        return final_df

    @abstractmethod
    def _read_data(self) -> tuple[dd.core.DataFrame, dd.core.DataFrame, dd.core.DataFrame]:


    def assign_split_names_to_data_frames_and_merge(
            self,
            train_df: dd.core.DataFrame,
            dev_df: dd.core.DataFrame,
            test_df: dd.core.DataFrame
            ) -> dd.core.DataFrame:
        train_df["split"] = "train"
        dev_df["split"] = "dev"
        test_df["split"] = "split"
        final_df = dd.concat([train_df, dev_df, test_df])
        return final_df

    def split_dataset(
            self,
            df: dd.core.DataFrame,
            test_size: float,
            stratify_column: Optional[str]
            ) -> tuple[dd.core.DataFrame, dd.core.DataFrame]:
        if stratify_column is None:
            return train_test_split(df, test_size=test_size, random_state=1234, shuffle=True)
        unique_column_values = df[stratify_column].unique()
        first_dfs = []
        second_dfs = []
        for unique_set_value in unique_column_values:
            # Workaround since dask does not have stratify option
            sub_df = df[df[stratify_column] == unique_set_value]
            sub_first_df, sub_second_df = train_test_split(sub_df, test_size=test_size, random_state=1234, shuffle=True)
            first_dfs.append(sub_first_df)
            second_df.append(sub_second_df)

        first_df = dd.concat(first_dfs)
        second_df = dd.concat(second_dfs)
        return first_df, second_df

    def get_remote_url(
            self,
            dataset_path: str
            ) -> str:
        dataset_url = get_url(path=dataset_path, repo=self.dvc_remote_repo, rev=self.version)
        return dataset_url


class GHCDatasetReader(DatasetReader):
    def __init__(
        self,
        dataset_dir: str,
        dataset_name: str,
        dev_split_ratio: float,
        gcp_project_id: str,
        gcp_github_access_token_secret_id: str,
        dvc_remote_repo: str,
        github_user_name: str,
        version: str,
    ) -> None:
        super().__init__(
            dataset_dir,
            dataset_name,
            gcp_project_id,
            gcp_github_access_token_secret_id,
            dvc_remote_repo,
            github_user_name,
            version,
        )
        self.dev_split_ratio = dev_split_ratio

    def _read_data(self) -> tuple[dd.core.DataFrame, dd.core.DataFrame, dd.core.DataFrame]:
        train_tsv_path = os.path.join(self.dataset_dir, "ghc_train.tsv")
        train_tsv_url = self.get_remote_data_url(train_tsv_path)
        train_df = dd.read_csv(train_csv_url, sep="\t", header=0)

        test_tsv_path = os.path.join(self.dataset_dir, "ghc_test.tsv")
        test_tsv_url = self.get_remote_data_url(test_tsv_path)
        test_df = dd.read_csv(train_csv_url, sep="\t", header=0)

        train_df["label"] = (train_df["hd"] + train_df["cv"] + train_df["vo"] > 0).astype(int)
        test_df["label"] = (test_df["hd"] + test_df["cv"] + test_df["vo"] > 0).astype(int)

        train_df, dev_df = self.split_dataset(train_df, self.dev_split_ratio, stratify_column="label")

        return train_df, dev_df, test_df
